import json
import logging
import os
from typing import Optional

import httpx

logger = logging.getLogger(__name__)


class SciPhi:
    def __init__(
        self,
        api_base: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 30,
    ):
        self.api_base = (
            api_base or os.getenv("SCIPHI_API_BASE") or "https://api.sciphi.ai"
        )
        self.api_key = api_key or os.getenv("SCIPHI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "You must specify an explicit api_key or define `SCIPHI_API_KEY` to initialize a SciPhi client."
            )
        self.timeout = timeout
        self.client = httpx.Client(
            base_url=self.api_base,
            headers=self._auth_headers(),
            timeout=timeout,
        )

    def _auth_headers(self):
        """
        Generate the authorization headers.
        """
        return {"Authorization": f"Bearer {self.api_key}"}

    def _handle_response(self, response: httpx.Response):
        if response.is_error:
            # Handle errors appropriately
            raise Exception(
                f"API request failed with status {response.status_code}"
            )
        return response.json()

    def search(self, provider: str, query: str):
        url = f"/search"
        payload = {"provider": provider, "query": query}
        response = self.client.post(url, json=payload)
        return self._handle_response(response)

    def get_search_rag_response(
        self,
        query: str,
        search_provider: str,
        llm_model: str = "SciPhi/Sensei-7B-V1",
        temperature: int = 0.2,
        top_p: int = 0.95,
    ):
        url = f"/search_rag"
        payload = {
            "query": query,
            "search_provider": search_provider,
            "llm_model": llm_model,
            "temperature": temperature,
            "top_p": top_p,
        }
        response = self.client.post(url, json=payload)
        handled_response = self._handle_response(response)
        for result in handled_response["search_results"]:
            if "score" in result:
                result["score"] = float(result["score"])
            if "metadata" in result:
                result["metadata"] = (
                    json.loads(result["metadata"]) if result["metadata"] != "" else {}
                )
        return handled_response

    def completion(
        self, path: str, method: str, headers: dict, body: dict
    ):
        url = f"/v1/{path}"
        response = self.client.request(
            method=method, url=url, headers=headers, json=body
        )
        return self._handle_response(response)

    def close(self):
        self.client.close()
