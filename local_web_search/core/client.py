from typing import List

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
    def __init__(self, api_base: str):
        self.api_base = api_base

    def search(
        self,
        query: str,
        num_step0_results: int = 100,
        num_step1_results: int = 25,
        num_step2_results: int = 10,
    ) -> List[SERPResult]:
        payload = {
            "query": query,
            "num_step0_results": num_step0_results,
            "num_step1_results": num_step1_results,
            "num_step2_results": num_step2_results,
        }
        response = requests.post(f"{self.api_base}/search", json=payload)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

        results = response.json().get("results", [])
        return [SERPResult.from_dict(result) for result in results]
