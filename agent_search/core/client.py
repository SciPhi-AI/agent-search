import os
from typing import List, Optional

import requests


class SERPResult:
    def __init__(
        self,
        score: float,
        url: str,
        title: str,
        dataset: str,
        metadata: dict,
        text: str,
    ):
        self.score = score
        self.url = url
        self.title = title
        self.dataset = dataset
        self.metadata = metadata
        self.text = text.strip()
        if self.title and self.text.startswith(self.title):
            self.text = self.text[len(self.title) :].strip()

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class SERPClient:
    def __init__(
        self, api_base: Optional[str] = None, auth_token: Optional[str] = None
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
        num_step0_results: int = 100,
        num_step1_results: int = 25,
        num_step2_results: int = 10,
    ) -> List[SERPResult]:
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "query": query,
            "num_step0_results": num_step0_results,
            "num_step1_results": num_step1_results,
            "num_step2_results": num_step2_results,
        }
        response = requests.post(
            f"{self.api_base}/search", headers=headers, json=payload
        )
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

        results = response.json()
        return [SERPResult.from_dict(result) for result in results]
