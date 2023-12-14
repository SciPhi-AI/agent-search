"""A script to populate the database with the given dataset and subset."""
import json
import logging
import multiprocessing
import os
import queue
import threading
import uuid

import fire
import numpy as np
import psycopg2
from datasets import load_dataset
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct

from agent_search.core.utils import load_config

logger = logging.getLogger(__name__)


def fetch_batch(pg_conn, table_name, start, end):
    logger.info(f"Fetching batch form {start} to {end}")
    pg_cursor = pg_conn.cursor()
    pg_cursor.execute(
        f"SELECT * FROM {table_name} OFFSET %s LIMIT %s", (start, end - start)
    )
    batch = pg_cursor.fetchall()
    pg_cursor.close()
    return batch


def qdrant_writer(qclient, collection_name, qdrant_queue):
    # SQLite and Qdrant setup
    logger.info("Launching Qdrant writer")
    while True:
        try:
            points = qdrant_queue.get()
            logger.info(f"Starting Qdrant write-out...")
            if points is None:  # Sentinel to end the process
                break
            operation_result = qclient.upsert(
                collection_name=collection_name,
                wait=True,
                points=points,
            )
            logger.info(f"Finished Qdrant write-out with result {operation_result}...")
        except Exception as e:
            logger.info(f"Task failed with {e}")


class PopulatePostgres:
    def __init__(self):
        self.config = load_config()["agent_search"]

    def run(self, batch_size=1_024, embedding_vec_size=768):
        logger.info(
            f"Initializing Qdrant Writer on collection {self.config['qdrant_collection_name']}..."
        )
        qclient = QdrantClient(
            self.config["qdrant_host"],
            port=self.config["qdrant_grpc_port"],
            prefer_grpc=self.config["qdrant_prefer_grpc"],
        )

        qdrant_queue = multiprocessing.Queue()
        qdrant_writer_thread = multiprocessing.Process(
            target=qdrant_writer,
            args=(
                qclient,
                self.config["qdrant_collection_name"],
                qdrant_queue,
            ),
        )
        qdrant_writer_thread.start()

        logger.info(
            f"Initializing Postgres connection with table {self.config['postgres_table_name']}..."
        )
        pg_conn = psycopg2.connect(
            dbname=self.config["postgres_db"],
            user=self.config["postgres_user"],
            password=self.config["postgres_password"],
            host=self.config["postgres_host"],
            options="-c client_encoding=UTF8",
        )
        cur = pg_conn.cursor()

        # Start a transaction
        cur.execute("BEGIN")

        # Declare a server-side cursor
        cur.execute(
            f"DECLARE my_cursor CURSOR FOR SELECT * FROM {self.config['postgres_table_name']}"
        )
        offset = 0
        while True:
            # Fetch a batch of rows
            logger.info(f"Fetching batch at index {offset}")
            cur.execute(f"FETCH {batch_size} FROM my_cursor")
            rows = cur.fetchall()
            offset += len(rows)
            if len(rows) == 0:
                break
            qdrant_points = []
            for row in rows:
                id, url, embeddings_binary, text_chunks, title, metadata = row
                embeddings = np.frombuffer(
                    embeddings_binary, dtype=np.float32
                ).reshape(-1, embedding_vec_size)

                text_chunks = json.loads(text_chunks)
                # Prepare data for Qdrant
                qdrant_points.extend(
                    [
                        PointStruct(
                            id=str(uuid.uuid3(uuid.NAMESPACE_DNS, url)),
                            vector=[float(ele) for ele in embedding],
                            payload={"text": text_chunks[i], "url": url},
                        )
                        for i, embedding in enumerate(embeddings)
                    ]
                )
            print("putting into queue...")
            qdrant_queue.put(qdrant_points)
        qdrant_queue.put(None)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)
    fire.Fire(PopulatePostgres)
