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

EMBEDDING_VEC_SIZE = 768


def process_rows(rows, output_queue):
    """Process the rows into qdrant point objects."""
    qdrant_points = []
    for row in rows:
        id, url, embeddings_binary, text_chunks, title, metadata = row
        embeddings = np.frombuffer(
            embeddings_binary, dtype=np.float32
        ).reshape(-1, EMBEDDING_VEC_SIZE)

        text_chunks = json.loads(text_chunks)
        # Prepare data for Qdrant
        qdrant_points.append(
            PointStruct(
                id=str(uuid.uuid3(uuid.NAMESPACE_DNS, url)),
                vector=[float(ele) for ele in embeddings[0]],
                payload={"text": text_chunks[0], "url": url},
            )
        )

    output_queue.put(qdrant_points)


def qdrant_writer(config, qdrant_queue):
    """A writer that listens for output events in a separate thread."""
    qclient = QdrantClient(
        config["qdrant_host"],
        port=config["qdrant_grpc_port"],
        prefer_grpc=config["qdrant_prefer_grpc"],
    )

    logger.info("Launching Qdrant writer")
    while True:
        try:
            points = qdrant_queue.get()
            logger.info(f"Starting Qdrant write-out...")
            if points is None:  # Sentinel to end the process
                break
            operation_result = qclient.upsert(
                collection_name=config["qdrant_collection_name"],
                wait=True,
                points=points,
            )
            logger.info(
                f"Finished Qdrant write-out with result {operation_result}..."
            )
        except Exception as e:
            logger.info(f"Task failed with {e}")


def process_batches(config, start, end, batch_size, output_queue):
    """Processes the batches in steps of the given batch_size"""

    # Connect to the database
    conn = psycopg2.connect(
        dbname=config["postgres_db"],
        user=config["postgres_user"],
        password=config["postgres_password"],
        host=config["postgres_host"],
        options="-c client_encoding=UTF8",
    )
    cur = conn.cursor()
    # Declare a server-side cursor with offset
    cur.execute(
        f"DECLARE proc_cursor CURSOR FOR SELECT * FROM {config['postgres_table_name']} OFFSET {start} LIMIT {end - start}"
    )

    offset = start
    while True:
        logger.info(f"Fetching a batch of size {batch_size} at offset {offset}")
        # Fetch a batch of rows
        cur.execute(f"FETCH {batch_size} FROM proc_cursor")
        rows = cur.fetchall()

        
        if len(rows) == 0:
            break        

        process_rows(rows, output_queue)
        offset += batch_size
        
        # terminate
        if len(rows) < batch_size:
            break        

    cur.close()
    conn.close()


class PopulateQdrant:
    def __init__(self):
        self.config = load_config()["agent_search"]

    def run(self, num_processes=16, batch_size=1_024):
        """Runs the population process for the qdrant database"""
        qdrant_queue = multiprocessing.Queue()
        qdrant_writer_thread = multiprocessing.Process(
            target=qdrant_writer,
            args=(
                self.config,
                qdrant_queue,
            ),
        )
        qdrant_writer_thread.start()

        conn = psycopg2.connect(
            dbname=self.config["postgres_db"],
            user=self.config["postgres_user"],
            password=self.config["postgres_password"],
            host=self.config["postgres_host"],
            options="-c client_encoding=UTF8",
        )
        cur = conn.cursor()

        # Count total number of entries
        cur.execute(f"SELECT COUNT(*) FROM {self.config['postgres_table_name']}")
        total_count = cur.fetchone()[0]
        logger.info(f"Processing {total_count} entries in {num_processes} processes")
        
        range_size = total_count // num_processes

        # Create and start multiprocessing workflow
        processes = []
        for i in range(num_processes):
            logger.info(f"Starting process {i}...")
            start = i * range_size
            end = start + range_size if i < num_processes - 1 else total_count
            proc = multiprocessing.Process(
                target=process_batches,
                args=(
                    self.config,
                    start,
                    end,
                    batch_size,
                    qdrant_queue,
                ),
            )
            processes.append(proc)
            proc.start()

        # Wait for all processes to finish
        for proc in processes:
            proc.join()

        cur.close()
        conn.close()
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)
    fire.Fire(PopulateQdrant)
