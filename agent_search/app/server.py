import logging
import time
from typing import Optional

from pydantic import BaseModel

from agent_search.core.utils import load_config, select_top_urls
from agent_search.search import WebSearchEngine

# Attempt to import uvicorn and FastAPI
try:
    import uvicorn
    from fastapi import FastAPI, HTTPException
except ImportError as e:
    raise ImportError(
        f"Error: {e}, Note - both uvicorn and FastAPI are required to run the server."
    )


logger = logging.getLogger(__name__)


class SearchServer:
    def __init__(self):
        self.client = WebSearchEngine()

    def run(
        self,
        query="What is a lagrangian?",
        limit_broad_results=1_000,
        limit_deduped_url_results=50,
        limit_hierarchical_url_results=50,
        limit_final_pagerank_results=20,
        url_contains_filter=None,
    ):
        """Run a search query using the WebSearchEngine client"""

        query_vector = self.client.get_query_vector(query)

        broad_results = self.client.similarity_search(
            query_vector=query_vector, limit=limit_broad_results
        )

        if not url_contains_filter:
            url_contains_filter = []

        deduped_url_results = select_top_urls(
            broad_results,
            max_urls=limit_deduped_url_results,
            url_contains=url_contains_filter,
        )

        hierarchical_url_results = (
            self.client.hierarchical_similarity_reranking(
                query_vector=query_vector,
                urls=deduped_url_results,
                limit=limit_hierarchical_url_results,
            )
        )

        pagerank_reranked_results = self.client.pagerank_reranking(
            hierarchical_url_results
        )[:limit_final_pagerank_results]

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


def check_limits(query: SearchQuery):
    """Check if the limit parameters exceed three times their default values"""
    if query.limit_broad_results > 3 * 1_000:
        raise ValueError(
            "limit_broad_results exceeds 3 times its default value"
        )
    if query.limit_deduped_url_results > 3 * 100:
        raise ValueError(
            "limit_deduped_url_results exceeds 3 times its default value"
        )
    if query.limit_hierarchical_url_results > 3 * 25:
        raise ValueError(
            "limit_hierarchical_url_results exceeds 3 times its default value"
        )
    if query.limit_final_pagerank_results > 3 * 10:
        raise ValueError(
            "limit_final_pagerank_results exceeds 3 times its default value"
        )


@app.post("/search")
def run_search(query: SearchQuery):
    """Run a search query"""
    try:
        check_limits(query)
        results = search_runner.run(
            query=query.query,
            limit_broad_results=query.limit_broad_results,
            limit_deduped_url_results=query.limit_deduped_url_results,
            limit_hierarchical_url_results=query.limit_hierarchical_url_results,
            limit_final_pagerank_results=query.limit_final_pagerank_results,
        )
        return {"results": results}
    except ValueError as e:
        logger.error(f"ValueError {e} = ", e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Exception {e} = ", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


if __name__ == "__main__":
    config = load_config()["server"]
    logging.basicConfig(level=config["log_level"])
    uvicorn.run(app, host=config["host"], port=int(config["port"]))
