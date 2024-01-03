import os
from typing import List, Optional

import requests

from .search_types import AgentSearchResult


class AgentSearchClient:
    def __init__(
        self,
        api_base: Optional[str] = None,
        auth_token: Optional[str] = None,
    ):
        self.api_base = (
            api_base or os.getenv("SCIPHI_API_BASE") or "https://api.sciphi.ai"
        )
        self.auth_token = auth_token or os.getenv("SCIPHI_API_KEY")

        if not self.auth_token:
            raise ValueError(
                "No authorization token provided and SCIPHI_API_KEY environment variable is not set."
            )

    def search(
        self,
        query: str,
        limit_broad_results: int = 1_000,
        limit_deduped_url_results: int = 100,
        limit_hierarchical_url_results: int = 25,
        limit_final_pagerank_results: int = 10,
    ) -> List[AgentSearchResult]:
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "query": query,
            "limit_broad_results": limit_broad_results,
            "limit_deduped_url_results": limit_deduped_url_results,
            "limit_hierarchical_url_results": limit_hierarchical_url_results,
            "limit_final_pagerank_results": limit_final_pagerank_results,
        }
        response = requests.post(
            f"{self.api_base}/search", headers=headers, json=payload
        )
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
        results = response.json()

        serp_results = [
            AgentSearchResult.from_dict(result) for result in results
        ]

        return serp_results
