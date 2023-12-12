import logging
import time
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agent_search.core.utils import load_config, select_top_urls
from agent_search.search import OpenWebSearch

logger = logging.getLogger(__name__)


def timed_fn(fn):
    """A decorator to time a function"""

    def wrapper(*args, **kwargs):
        t0 = time.time()
        result = fn(*args, **kwargs)
        t1 = time.time()
        logger.debug(f"Time taken for {fn.__name__}: {t1 - t0}")
        return result

    return wrapper


class SearchServer:
    def __init__(self):
        self.client = OpenWebSearch()

    def run(
        self,
        query="What is a lagrangian?",
        limit_broad_results=1_000,
        limit_deduped_url_results=50,
        limit_hierarchical_url_results=20,
        limit_final_pagerank_results=10,
        url_contains_filter=None,
    ):
        """Run a search query using the OpenWebSearch client"""
        query_vector = self.client.get_query_vector(query)
        broad_results = timed_fn(self.client.similarity_search)(
            query_vector=query_vector, limit=limit_broad_results
        )
        logger.debug(
            f"Step 0: Broad similarity search, {len(broad_results)} results"
        )

        if not url_contains_filter:
            url_contains_filter = []

        deduped_url_results = select_top_urls(
            broad_results,
            max_urls=limit_deduped_url_results,
            url_contains=url_contains_filter,
        )

        logger.debug(
            f"Step 1: Unique URL Filtration, {len(deduped_url_results)} results"
        )

        hierarchical_url_results = timed_fn(
            self.client.hierarchical_similarity_reranking
        )(
            query_vector=query_vector,
            urls=deduped_url_results,
            limit=limit_hierarchical_url_results,
        )

        logger.debug(
            f"Step 2: Reranking using hierarchical similarity search, {len(hierarchical_url_results)} results returned"
        )

        try:
            pagerank_reranked_results = timed_fn(
                self.client.pagerank_reranking
            )(hierarchical_url_results)[:limit_final_pagerank_results]
            logger.debug(
                "Step 3: Reranking using pagerank, {len(pagerank_reranked_results)} results returned"
            )

            # Print or process the sorted results
            for serp_result in pagerank_reranked_results:
                logger.debug(
                    f"URL: {serp_result.url}, Similarity: {serp_result.score:.4f}:\nTitle: {serp_result.title}\nText:\n{serp_result.text}"
                )
                logger.debug("-" * 100)
        except Exception as e:
            logger.error(
                f"An error occurred while reranking using pagerank: {e}"
            )

        return pagerank_reranked_results


class SearchQuery(BaseModel):
    """A search query data model"""

    query: str
    limit_broad_results: Optional[int] = 1_000
    limit_deduped_url_results: Optional[int] = 100
    limit_hierarchical_url_results: Optional[int] = 25
    limit_final_pagerank_results: Optional[int] = 10


app = FastAPI()
search_runner = SearchServer()


@app.post("/search")
def run_search(query: SearchQuery):
    """Run a search query"""
    try:
        results = search_runner.run(
            query=query.query,
            limit_broad_results=query.limit_broad_results,
            limit_deduped_url_results=query.limit_deduped_url_results,
            limit_hierarchical_url_results=query.limit_hierarchical_url_results,
            limit_final_pagerank_results=query.limit_final_pagerank_results,
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    config = load_config()["server"]
    logging.basicConfig(level=config["log_level"])
    uvicorn.run(app, host=config["host"], port=int(config["port"]))
