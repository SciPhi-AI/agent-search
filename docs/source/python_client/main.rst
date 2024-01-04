SciPhi API Client Documentation
===============================

Introduction
------------

The SciPhi API Client is a Python library for interacting with the SciPhi API. It provides methods for performing searches, retrieving search RAG responses, generating completions, and managing client sessions.

Classes and Methods
-------------------

`SciPhi` Class
.. class:: :white:`SciPhi`

   `SciPhi` Client for interacting with the SciPhi API.

   Attributes:
      api_base (str): Base URL for the SciPhi API.
      api_key (str): API key for authenticating requests.
      timeout (int): Timeout for API requests in seconds.
      client (httpx.Client): HTTP client for making requests.

   .. method:: __init__(self, api_base: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 30)

      Initializes the SciPhi client.

      :param api_base: Optional[str]: Base URL for the SciPhi API.
      :param api_key: Optional[str]: API key for authenticating requests.
      :param timeout: int: Timeout for API requests in seconds.
      :raises ValueError: If `api_key` is not provided.

   .. method:: _auth_headers(self) -> Dict[str, str]

      Generates the authorization headers for the API requests.

      :return: Dict[str, str]: Authorization headers with bearer token.

   .. method:: _handle_api_response(self, response: httpx.Response) -> Dict

      Handles the HTTP response from the API.

      :param response: httpx.Response: The response from the API request.
      :return: Dict: JSON response content.
      :raises Exception: If the response indicates an error.

   .. method:: _handle_search_response(self, search_results: Dict[str, str]) -> None

      Handles dictionary search responses from the API.

      :param search_results: Dict[str, str]: The response from the API request.
      :return: Dict: JSON response content.
      :raises Exception: If the response indicates an error.

   .. method:: search(self, query: str, search_provider: str) -> List[Dict]

      Performs a search query using the SciPhi API.

      :param query: str: The search query string.
      :param search_provider: str: The search provider to use.
      :return: List[Dict]: A list of search results.

   .. method:: get_search_rag_response(self, query: str, search_provider: str, llm_model: str = "SciPhi/Sensei-7B-V1", temperature: int = 0.2, top_p: int = 0.95)

      Retrieves a search RAG (Retrieval-Augmented Generation) response from the API.

      :param query: str: The search query string.
      :param search_provider: str: The search provider to use.
      :param llm_model: str: The language model to use.
      :param temperature: int: The temperature setting for the query.
      :param top_p: int: The top-p setting for the query.
      :return: Dict: A dictionary with the search response and related queries.

   .. method:: completion(self, prompt: str, llm_model_name: str = "SciPhi/Sensei-7B-V1", llm_max_tokens_to_sample: int = 1_024, llm_temperature: float = 0.2, llm_top_p: float = 0.90) -> SearchRAGResponse

      Generates a completion for a given prompt using the SciPhi API.

      :param prompt: str: The prompt for generating completion.
      :param llm_model_name: str: The language model to use.
      :param llm_max_tokens_to_sample: int: Maximum number of tokens for the sample.
      :param llm_temperature: float: The temperature setting for the query.
      :param llm_top_p: float: The top-p setting for the query.
      :return: Dict: A dictionary containing the generated completion.
      :raises ImportError: If the `sciphi-synthesizer` package is not installed.

   .. method:: close(self) -> None

      Closes the HTTP client.

Use and Examples
----------------

The SciPhi API Client is designed to simplify interaction with the SciPhi API. It abstracts the complexities of HTTP requests and response handling, providing a convenient interface for Python developers.

Example usage:

.. code-block:: python

   from sciphi import SciPhi

   # Initialize the client
   client = SciPhi(api_key="your_api_key")

   # Perform a search
   search_results = client.search("quantum computing", "wikipedia")

   # Retrieve a search RAG response
   rag_response = client.get_search_rag_response("natural language processing", "bing")

   # Generate a completion
   completion = client.completion("Explain the Turing Test", llm_model_name="SciPhi/Sensei-7B-V1

   # Close the client
   client.close()

By encapsulating the details of the API calls, the SciPhi API Client offers a user-friendly way to leverage the advanced search and AI capabilities of the SciPhi platform.