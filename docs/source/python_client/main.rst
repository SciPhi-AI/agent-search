SciPhi API Client Documentation
===============================

Introduction
------------

The SciPhi API Client is a Python library for interacting with the SciPhi API. It provides methods for performing searches, retrieving search RAG responses, generating completions, and managing client sessions.


Use and Examples
----------------

The SciPhi API Client is designed to simplify interaction with the SciPhi API. It abstracts the complexities of HTTP requests and response handling, providing a convenient interface for Python developers.


Call a pre-configured search agent endpoint:

   .. code-block:: python

      # Requires SCIPHI_API_KEY in the environment
      from agent_search import SciPhi

      client = SciPhi()

      # Search, then summarize result and generate related queries
      agent_summary = client.get_search_rag_response(query='latest news', search_provider='bing', llm_model='SciPhi/Sensei-7B-V1')
      print(agent_summary)
      # {'response': "The latest news encompasses ... and its consequences [2].", 'related_queries': ['Details on the...', ...], 'search_results' : [...]}

Standalone searches and from the AgentSearch search engine are supported:

   .. code-block:: python
      
      from agent_search import SciPhi

      client = SciPhi()

      # Perform a search
      search_response = client.search(query='Quantum Field Theory', search_provider='agent-search')

      print(search_response)
      # [{ 'score': '.89', 'url': 'https://...', 'metadata': {...} }

Code your own custom search agent workflow:

   .. code-block:: python
      
      from agent_search import SciPhi
      import json

      client = SciPhi()

      # Specify instructions for the task
      instruction = "Your task is to perform retrieval augmented generation (RAG) over the given query and search results. Return your answer in a json format that includes a summary of the search results and a list of related queries."
      query = "What is Fermat's Last Theorem?"

      # construct search context
      search_response = client.search(query=query, search_provider='agent-search')
      search_context = "\n\n".join(
          f"{idx + 1}. Title: {item['title']}\nURL: {item['url']}\nText: {item['text']}"
          for idx, item in enumerate(search_response)
      ).encode('utf-8')
    
      # Prefix to enforce a JSON response 
      json_response_prefix = '{"summary":'
      
      # Prepare a prompt
      formatted_prompt = f"### Instruction:{instruction}\n\nQuery:\n{query}\n\nSearch Results:\n${search_context}\n\nQuery:\n{query}\n### Response:\n{json_response_prefix}",

      # Generate a raw string completion with Sensei-7B-V1
      completion = json_response_prefix + client.completion(formatted_prompt, llm_model_name="SciPhi/Sensei-7B-V1")

      print(json.loads(completion))
      # {
      #   "summary":  "\nFermat's Last Theorem is a mathematical proposition first prop ... ",
      #   "other_queries": ["The role of elliptic curves in the proof of Fermat's Last Theorem", ...]
      # }



By encapsulating the details of the API calls, the SciPhi API Client offers a user-friendly way to leverage the advanced search and AI capabilities of the SciPhi platform.
Classes and Methods
-------------------

.. class:: SciPhi

    Client for interacting with the SciPhi API.

    Attributes:
        api_base (str): Base URL for the SciPhi API.
        api_key (str): API key for authenticating requests.
        timeout (int): Timeout for API requests in seconds.
        client (httpx.Client): HTTP client for making requests.

    .. method:: search(self, query: str, search_provider: str) -> List[Dict]

        Performs a search query using the SciPhi API.

        :param query: str: The search query string.
        :param search_provider: str: The search provider to use.
        :return: List[Dict]: A list of search results w/ fields that correspond with `SearchResult`, specified below.

    .. method:: get_search_rag_response(self, query: str, search_provider: str, llm_model: str = "SciPhi/Sensei-7B-V1", temperature: int = 0.2, top_p: int = 0.95)

        Retrieves a search RAG (Retrieval-Augmented Generation) response from the API.

        :param query: str: The search query string.
        :param search_provider: str: The search provider to use.
        :param llm_model: str: The language model to use.
        :param temperature: int: The temperature setting for the query.
        :param top_p: int: The top-p setting for the query.
        :return: str: A string containing the completed text.

    .. method:: completion(self, prompt: str, llm_model_name: str = "SciPhi/Sensei-7B-V1", llm_max_tokens_to_sample: int = 1_024, llm_temperature: float = 0.2, llm_top_p: float = 0.90) -> str

        Generates a completion string for a given prompt using the SciPhi API.

        :param prompt: str: The prompt for generating completion.
        :param llm_model_name: str: The language model to use.
        :param llm_max_tokens_to_sample: int: Maximum number of tokens for the sample.
        :param llm_temperature: float: The temperature setting for the query.
        :param llm_top_p: float: The top-p setting for the query.
        :return: Dict: A dictionary containing the generated completion.
        :raises ImportError: If the `sciphi-synthesizer` package is not installed.

    .. method:: close(self) -> None

        Closes the HTTP client.


Model Classes
-------------

.. class:: SearchResult

    Represents a single search result.

    .. attribute:: score

        The score of the search result.
    
    .. attribute:: title

        The title of the search result.

    .. attribute:: text

        The raw text of the search result.

    .. attribute:: url

        The URL of the search result.

    .. attribute:: metadata

        Optional metadata for the search result.

.. class:: SearchRAGResponse

    Represents the response from a search or RAG query.

    .. attribute:: response

        The response text.

    .. attribute:: related_queries

        A list of related queries.

    .. attribute:: search_results

        A list of SearchResult objects.
