import csv
import json
import logging
import os
from typing import List

import numpy as np
from qdrant_client import QdrantClient
from transformers import AutoModel

from agent_search.core import SERPResult
from agent_search.core.utils import (
    cosine_similarity,
    get_data_path,
    load_config,
)

logger = logging.getLogger(__name__)


class WebSearchEngine:
    """A simple search client for the OpenSearch collection"""

    def __init__(
        self,
    ):
        try:
            import psycopg2
        except ImportError as e:
            raise ImportError(
                f"Error {e} while imoprting psycopg2. Please install it with `pip install psycopg2` to run an WebSearchEngine instance."
            )

        # Load config
        self.config = load_config()["agent_search"]

        # Load Postgres
        logger.info(
            f"Connecting to Postgres database at: {self.config['postgres_db']}."
        )
        self.conn = psycopg2.connect(
            dbname=self.config["postgres_db"],
            user=self.config["postgres_user"],
            password=self.config["postgres_password"],
            host=self.config["postgres_host"],
            options="-c client_encoding=UTF8",
        )
        self.cur = self.conn.cursor()

        # Load qdrant client
        logger.info(
            f"Connecting to collection: {self.config['qdrant_collection_name']}"
        )
        self.qdrant_collection_name = self.config["qdrant_collection_name"]
        self.client = QdrantClient(
            self.config["qdrant_host"],
            grpc_port=self.config["qdrant_grpc_port"],
            prefer_grpc=True,
        )
        if not self.client.get_collection(self.qdrant_collection_name):
            raise ValueError(
                f"Must have a Qdrant collection with the name {self.qdrant_collection_name}."
            )

        # Load embedding model
        self.embedding_model = AutoModel.from_pretrained(
            self.config["embedding_model_name"], trust_remote_code=True
        )

        self.pagerank_rerank_module = self.config["pagerank_rerank_module"]
        pagerank_file_path = self.config["pagerank_file_path"]
        if self.pagerank_rerank_module:
            if not pagerank_file_path:
                # Simulating reading from a CSV file
                pagerank_file_path = os.path.join(
                    get_data_path(), "domain_ranks.csv"
                )

                if not os.path.exists(pagerank_file_path):
                    raise ValueError(
                        "Must have a pagerank file at the config specified path when using pagerank_rerank_module"
                    )

            self.pagerank_importance = float(
                self.config["pagerank_importance"]
            )
            self.domain_to_rank_map = {}

            with open(pagerank_file_path, newline="") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    domain = row["Domain"]
                    rank = float(row["Open Page Rank"])
                    self.domain_to_rank_map[domain] = rank

    def get_query_vector(self, query: str):
        """Gets the query vector for the given query"""

        query_vector = self.embedding_model.encode(query)
        return query_vector

    def similarity_search(
        self,
        query_vector: np.ndarray,
        limit: int = 100,
    ):
        """Searches the collection for the given query and returns the top 'limit' results"""

        points = self.client.search(
            collection_name=self.qdrant_collection_name,
            query_vector=query_vector,
            limit=limit,
        )

        return [
            SERPResult(
                score=point.score,
                text=point.payload["text"],
                title=None,
                url=point.payload["url"],
                metadata={},
            )
            for point in points
        ]

    def hierarchical_similarity_reranking(
        self,
        query_vector: np.ndarray,
        urls: List[str],
        limit: int = 100,
    ) -> List[SERPResult]:
        """Hierarchical URL search to find the most similar text chunk for the given query and URLs"""
        # SQL query to fetch the entries for the URLs
        # Assuming 'urls' is a list of URL strings
        query = f"SELECT url, title, metadata, dataset, text_chunks, embeddings FROM {self.config['postgres_table_name']} WHERE url IN %s"
        # Fetch all results
        self.cur.execute(query, (tuple(urls),))
        results = self.cur.fetchall()

        # List to store the results along with their similarity scores
        similarity_results = []

        # Iterate over each result to find the most similar text chunk
        for result in results:
            (
                url,
                title,
                metadata,
                dataset,
                text_chunks_str,
                embeddings_binary,
            ) = result
            # deserialize the embeddings and text chunks
            embeddings = np.frombuffer(
                embeddings_binary, dtype=np.float32
            ).reshape(-1, 768)
            text_chunks = json.loads(text_chunks_str)
            max_similarity = -1e9
            most_similar_chunk = None

            # Iterate over each embedding to find the one with maximum cosine similarity
            for chunk, embedding in zip(text_chunks, embeddings):
                similarity = cosine_similarity(
                    np.array(query_vector), np.array(embedding)
                )
                if similarity > max_similarity:
                    max_similarity = similarity
                    most_similar_chunk = chunk

            # Store the most similar chunk and its similarity score
            similarity_results.append(
                SERPResult(
                    score=max_similarity,
                    url=url,
                    title=title,
                    metadata=json.loads(metadata),
                    dataset=dataset,
                    text=most_similar_chunk,
                ),
            )

        # Sort the results based on similarity score in descending order
        similarity_results.sort(key=lambda x: x.score, reverse=True)
        return similarity_results[:limit]

    def pagerank_reranking(
        self,
        similarity_results: List[SERPResult],
        limit: int = 100,
    ) -> List[SERPResult]:
        """Reranks the results based on the PageRank score of the domain"""
        if not self.pagerank_rerank_module:
            raise Exception(
                "PageRank reranking module is not enabled. Please set pagerank_rerank_module=True while initializing the WebSearchEngine client."
            )
        # List to store the results along with their PageRank scores
        pagerank_results = []

        # Iterate over each result to find the PageRank score of the domain
        for result in similarity_results:
            pagerank_score = 0
            try:
                domain = result.url.split("/")[2]
                pagerank_score = self.domain_to_rank_map.get(domain, 0)
            except Exception as e:
                logger.info(f"Error {e}: Found for URL: {result.url}")
            reweighted_score = (
                self.pagerank_importance * pagerank_score / 10.0
                + (1 - self.pagerank_importance) * result.score
            )
            pagerank_results.append(
                SERPResult(
                    score=reweighted_score,
                    url=result.url,
                    title=result.title,
                    metadata=result.metadata,
                    dataset=result.dataset,
                    text=result.text,
                )
            )

        # Sort the results based on PageRank score in descending order
        pagerank_results.sort(key=lambda x: x.score, reverse=True)
        return pagerank_results[:limit]
