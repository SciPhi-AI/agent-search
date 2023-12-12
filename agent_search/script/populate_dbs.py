"""A script to populate the database with the given dataset and subset."""
import json
import logging
import os
import queue
import sqlite3
import threading
import uuid

import fire
from datasets import load_dataset
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import PointStruct

from local_search.core.utils import load_config

logger = logging.getLogger(__name__)


# A function that will write out the points
# To be ran in a separate thread
def writer(o, config, qclient):
    logger.info("Starting writer...")
    i = 0
    while True:
        try:
            points = o.get()
            if points is None:
                break
            logger.info(f"Writing out...")
            operation_info = qclient.upsert(
                collection_name=config["qdrant_collection_name"],
                wait=True,
                points=points,
            )
            i += len(points)
            logger.info(
                f"i:{i}, n_points:{len(points)}, operation_info:{operation_info}"
            )

            o.task_done()
        except Exception as e:
            logger.info(f"Error: {e}")
            continue


def create_sqlite_table(conn, cursor, table_name) -> None:
    """Create the table in the database"""
    create_sqlite_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY,
        url TEXT UNIQUE,
        title TEXT,
        metadata TEXT,
        dataset TEXT,
        text_chunks TEXT,
        embeddings TEXT
    )
    """
    cursor.execute(create_sqlite_table_query)
    conn.commit()


def create_qdrant_collection(client, config) -> None:
    client.create_collection(
        collection_name=config["qdrant_collection_name"],
        vectors_config=models.VectorParams(
            size=768, distance=models.Distance.COSINE
        ),
        quantization_config=models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(
                type=models.ScalarType.INT8,
                quantile=0.99,
                always_ram=True,
            ),
        ),
    )


def insert_entry(conn, cursor, table_name, entry):
    """Insert the entry into the database"""

    # Serialize the embeddings list to a JSON string
    text_chunks_json = json.dumps(entry["text_chunks"])
    embeddings_json = json.dumps(entry["embeddings"])

    insert_query = f"""
    INSERT INTO {table_name} (id, url, title, metadata, dataset, text_chunks, embeddings) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    try:
        cursor.execute(
            insert_query,
            (
                entry["id"],
                entry["url"],
                entry["title"],
                entry["metadata"],
                entry["dataset"],
                text_chunks_json,
                embeddings_json,
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError as e:
        logger.warning(f"Error while inserting entry: {e}")


class Populate:
    """A class to populate the database with the given dataset and subset."""

    def __init__(self):
        self.config = load_config()["open_web_search"]

    def populate_sqlite(
        self,
        dataset="SciPhi/OpenWebSearch-V1",
        subset="arxiv",
        limit=10_000,
        log_interval=1_000,
    ) -> None:
        """Populate the database with the given dataset and subset"""
        if subset == "all":
            subset = "**"

        db_path = Populate.get_db_path(self.config)

        if not os.path.exists(os.path.dirname(db_path)):
            os.makedirs(os.path.dirname(db_path))

        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        sqlite_table_name = self.config["sqlite_table_name"]
        create_sqlite_table(conn, cur, sqlite_table_name)

        for counter, entry in enumerate(
            Populate.data_streamer(dataset, subset)
        ):
            insert_entry(conn, cur, sqlite_table_name, entry)
            if counter % log_interval == 0:
                logger.info(f"Inserted {counter} entries")
            if counter >= limit:
                break

        # Count the number of rows in the table
        cur.execute(f"SELECT COUNT(*) FROM {sqlite_table_name}")
        row_count = cur.fetchone()[0]
        logger.info(f"Number of rows in the table: {row_count}")

        # Calculate the size of the database file
        db_size = os.path.getsize(db_path)
        logger.info(f"Size of the database file: {db_size} bytes")

        # Close the database connection
        conn.close()

    def populate_qdrant(self, batch_size=100) -> None:
        """Populate the database with the given dataset and subset"""

        output_queue = queue.Queue()

        qdrant_client = QdrantClient(
            self.config["qdrant_client_host"],
            grpc_port=self.config["qdrant_client_grpc_port"],
            prefer_grpc=True,
        )

        writer_thread = threading.Thread(
            target=writer,
            args=(output_queue, self.config, qdrant_client),
        )
        writer_thread.start()

        db_path = Populate.get_db_path(self.config)
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        try:
            create_qdrant_collection(qdrant_client, self.config)
        except Exception as e:
            logger.warning(f"Error while creating collection: {e}")

        # Prepare the query to select entries from the SQLite database
        sqlite_table_name = self.config["sqlite_table_name"]
        select_query = f"SELECT * FROM {sqlite_table_name}"
        cur.execute(select_query)

        logger.info("Populating the Qdrant Collection...")
        while True:
            logger.info("Fetching rows from the SQLite database...")
            rows = cur.fetchmany(batch_size)

            if not rows:
                break

            # Process each row in the batch
            points = []
            for row in rows:
                # Extract and process data from the row
                (
                    _,
                    url,
                    __,
                    ___,
                    ____,
                    text_chunks,
                    embeddings,
                ) = row
                text_chunks_list = json.loads(text_chunks)
                embeddings_list = json.loads(embeddings)
                points.extend(
                    [
                        PointStruct(
                            id=str(uuid.uuid3(uuid.NAMESPACE_DNS, url)),
                            vector=embedding,
                            payload={"text": text_chunks_list[i], "url": url},
                        )
                        for i, embedding in enumerate(embeddings_list)
                    ]
                )

            output_queue.put(points)

            logger.info(f"Processed batch of {len(rows)} entries")

        output_queue.put(points)

        # Close the database connection
        conn.close()

    @staticmethod
    def get_db_path(config):
        return os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "..",
            config["sqlite_db_rel_path"],
        )

    @staticmethod
    def data_streamer(dataset, subset):
        """Stream the data from the given dataset and subset"""
        return load_dataset(
            dataset,
            data_files=f"{subset}/*",
            streaming=True,
        )["train"]


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)
    fire.Fire(Populate)
