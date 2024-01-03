SciPhi API Client Documentation
===============================

Introduction
------------

The SciPhi API Client is a Python library for interacting with the SciPhi API. It provides methods for performing searches, retrieving search RAG responses, generating completions, and managing client sessions.

Classes and Methods
-------------------

.. class:: SciPhi

    Client class for interacting with the SciPhi API.

    .. attribute:: api_base

        The base URL for the SciPhi API.

    .. attribute:: api_key

        The API key for authenticating requests.

    .. attribute:: timeout

        The timeout for API requests in seconds.

    .. attribute:: client

        The HTTP client for making requests.

    .. method:: search(query: str, search_provider: str) -> List[Dict]

        Performs a search query using the SciPhi API.

        :param query: The search query string.
        :param search_provider: The search provider to use.
        :return: A list of search results as dictionaries.

    .. method:: get_search_rag_response(query: str, search_provider: str, llm_model: str = "SciPhi/Sensei-7B-V1", temperature: int = 0.2, top_p: int = 0.95) -> Dict

        Retrieves a search RAG (Retrieval-Augmented Generation) response from the API.

        :param query: The search query string.
        :param search_provider: The search provider to use.
        :param llm_model: The language model to use (currently only "SciPhi/Sensei-7B-V1" is supported).
        :param temperature: The temperature setting for the query.
        :param top_p: The top-p setting for the query.
        :return: A dictionary with the search response and related queries.

    .. method:: close() -> None

        Closes the HTTP client.

Model Classes
-------------

.. class:: SearchResult

    Represents a single search result.

    .. attribute:: score

        The score of the search result.

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

Example Usage
-------------

Below are some example uses of the SciPhi API client.

.. code-block:: python

    from agent_search import SciPhi

    client = SciPhi()

    # Using Bing as the search provider
    rag_response = client.get_search_rag_response(
        query="synthetic biology", search_provider="bing", llm_model="SciPhi/Sensei-7B-V1"
    )
    print(rag_response)

    search = client.search(query="synthetic biology", search_provider="bing")
    print(search)

    # Using AgentSearch as the search provider
    rag_response = client.get_search_rag_response(
        query="synthetic biology",
        search_provider="agent-search",
        llm_model="SciPhi/Sensei-7B-V1",
    )
    print(rag_response)

    search = client.search(query="synthetic biology", search_provider="agent-search")
    print(search)
