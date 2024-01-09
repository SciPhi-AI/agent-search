import json
import logging
import os
from typing import Dict, List, Optional, Any

import httpx
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class SearchResult(BaseModel):
    score: Optional[float] = None
    url: str
    title: str
    text: str
    dataset: str
    metadata: Any


class SearchRAGResponse(BaseModel):
    response: str
    related_queries: List[str]
    search_results: List[SearchResult]


class SciPhi:
    """
    Client for interacting with the SciPhi API.

    Attributes:
        api_base (str): Base URL for the SciPhi API.
        api_key (str): API key for authenticating requests.
        timeout (int): Timeout for API requests in seconds.
        client (httpx.Client): HTTP client for making requests.
    """

    def __init__(
        self,
        api_base: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 30,
    ) -> None:
        """
        Initializes the SciPhi client.

        Args:
            api_base (Optional[str]): Base URL for the SciPhi API.
            api_key (Optional[str]): API key for authenticating requests.
            timeout (int): Timeout for API requests in seconds.

        Raises:
            ValueError: If `api_key` is not provided.
        """

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

    def _auth_headers(self) -> Dict[str, str]:
        """
        Generates the authorization headers for the API requests.

        Returns:
            Dict[str, str]: Authorization headers with bearer token.
        """

        return {"Authorization": f"Bearer {self.api_key}"}

    def _handle_api_response(self, response: httpx.Response) -> Dict:
        """
        Handles the HTTP response from the API.

        Args:
            response (httpx.Response): The response from the API request.

        Returns:
            Dict: JSON response content.

        Raises:
            Exception: If the response indicates an error.
        """

        if response.is_error:
            # Handle errors appropriately
            raise Exception(
                f"API request failed with status {response.status_code}"
            )
        result = response.json()
        return result

    def _handle_search_response(self, search_results: Dict[str, str]) -> None:
        """
        Handles dictionary search resopnses from the API.

        Args:
            search_results (Dict[str, str]): The response from the API request.

        Returns:
            Dict: JSON response content.

        Raises:
            Exception: If the response indicates an error.
        """

        for result in search_results:
            if "score" in result:
                result["score"] = float(result["score"])
            if "metadata" in result:
                try:
                    result["metadata"] = (
                        json.loads(result["metadata"])
                        if (
                            result["metadata"] != None
                            and result["metadata"] != '""'
                        )
                        else {}
                    )
                except Exception as e:
                    result["metadata"] = dict()

    def search(self, query: str, search_provider: str) -> List[Dict]:
        """
        Performs a search query using the SciPhi API.

        Args:
            query (str): The search query string.
            search_provider (str): The search provider to use.

        Returns:
            List[Dict]: A list of search results.
        """

        url = f"/search"
        payload = {"provider": search_provider, "query": query}
        response = self.client.post(url, json=payload)
        handled_response = self._handle_api_response(response)
        self._handle_search_response(handled_response)
        return [SearchResult(**ele).dict() for ele in handled_response]

    def get_search_rag_response(
        self,
        query: str,
        search_provider: str,
        llm_model: str = "SciPhi/Sensei-7B-V1",
        temperature: int = 0.2,
        top_p: int = 0.95,
    ):
        """
        Retrieves a search RAG (Retrieval-Augmented Generation) response from the API.

        Args:
            query (str): The search query string.
            search_provider (str): The search provider to use.
            llm_model (str): The language model to use.
            temperature (int): The temperature setting for the query.
            top_p (int): The top-p setting for the query.

        Returns:
            Dict: A dictionary with the search response and related queries.
        """

        if query == "":
            raise ValueError("Blank query submitted.")
        if search_provider not in ["bing", "agent-search"]:
            raise ValueError(f"Unsupported provider, {search_provider}")

        url = f"/search_rag"
        payload = {
            "query": query,
            "search_provider": search_provider,
            "llm_model": llm_model,
            "temperature": temperature,
            "top_p": top_p,
        }

        response = self.client.post(url, json=payload)
        handled_response = self._handle_api_response(response)

        # rename the other queries to `related_queries` until LLM output is re-factored.
        handled_response["related_queries"] = handled_response.pop(
            "other_queries"
        )

        self._handle_search_response(handled_response["search_results"])
        # Use Pydantic model for parsing and validation
        search_response = SearchRAGResponse(**handled_response)
        return search_response.dict()

    def completion(
        self,
        prompt: str,
        llm_model_name: str = "SciPhi/Sensei-7B-V1",
        llm_max_tokens_to_sample: int = 1_024,
        llm_temperature: float = 0.2,
        llm_top_p: float = 0.90,
    ) -> SearchRAGResponse:
        """
        Generates a completion for a given prompt using the SciPhi API.

        Args:
            prompt (str): The prompt for generating completion.
            llm_model_name (str): The language model to use.
            llm_max_tokens_to_sample (int): Maximum number of tokens for the sample.
            llm_temperature (float): The temperature setting for the query.
            llm_top_p (float): The top-p setting for the query.

        Returns:
            Dict: A dictionary containing the generated completion.

        Raises:
            ImportError: If the `sciphi-synthesizer` package is not installed.
        """

        try:
            import synthesizer
        except ImportError as e:
            raise ImportError(
                "Please install run `pip install sciphi-synthesizer` before attempting to generate a completion."
            )

        from synthesizer.core import LLMProviderName
        from synthesizer.interface import LLMInterfaceManager
        from synthesizer.llm import GenerationConfig

        llm_interface = LLMInterfaceManager.get_interface_from_args(
            LLMProviderName("sciphi"),
        )

        generation_config = GenerationConfig(
            model_name=llm_model_name,
            max_tokens_to_sample=llm_max_tokens_to_sample,
            temperature=llm_temperature,
            top_p=llm_top_p,
        )

        completion = '{"response":' + llm_interface.get_completion(
            prompt, generation_config
        ).replace("</s>", "")
        try:
            completion = json.loads(completion)

            # rename the other queries to `related_queries` until LLM output is re-factored.
            completion["related_queries"] = completion.pop("other_queries")

            return completion
        
        except Exception as e:
            return {'error': e}

    def close(self) -> None:
        """
        Closes the HTTP client.
        """

        self.client.close()
