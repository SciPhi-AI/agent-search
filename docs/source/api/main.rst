AgentSearch API Documentation
=============================

Welcome to the AgentSearch API documentation. Here, you'll find comprehensive details on how to use the various endpoints provided by the AgentSearch service. This API facilitates interaction with the powerful functionalities of the AgentSearch codebase and associated AI models.

Endpoint Overview
-----------------

1. **Search**: Fetches related search results for a given query, leveraging the AgentSearch framework and dataset.
2. **Completions**: Generates completions using `SciPhi/Sensei-7B-V1`, SciPhi's expert search agent.

Detailed Endpoint Descriptions
------------------------------

Search Endpoint
~~~~~~~~~~~~~~~

- **URL**: ``/search``
- **Method**: ``POST``
- **Description**: Accesses the Retriever module of the AgentSearch infrastructure, enabling searches for related documents based on queries.

**Request Body**:
  - ``query`` (str): The query string to be searched.

**Response**: 
A list of ``AgentSearchResult`` objects, each containing:
  - ``score`` (float): The relevance score of the document.
  - ``url`` (str): The document's URL.
  - ``title`` (str): The document's title.
  - ``text`` (str): The document's text content.
  - ``metadata`` (dict): Stringified JSON object with document metadata.
  - ``dataset`` (str): Dataset to which the document belongs.

**Example**:

.. code-block:: bash

   export SCIPHI_API_KEY=${MY_API_KEY}

   curl -X POST https://api.sciphi.ai/search \
        -H "Authorization: Bearer $SCIPHI_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"query": "What is quantum field theory in curved spacetime?"}'

**Response**:

.. code-block:: none

   [
    {
        "score": 0.9219,
        "url": "https://en.wikipedia.org/wiki/Quantum%20field%20theory%20in%20curved%20spacetime",
        "title": "Quantum field theory in curved spacetime",
        "dataset": "wikipedia",
        "text": "These theories rely on general relativity...",
        "metadata": {},
    },
    ... Additional results ...
   ]

LLM Endpoints
~~~~~~~~~~~~~

SciPhi adheres to OpenAI's API specification, ensuring compatibility with applications designed for OpenAI.

**Example**:

.. code-block:: bash

    export SEARCH_CONTEXT="N/A"
    export PREFIX='{"response":'

    curl https://api.sciphi.ai/v1/completions \
      -H "Content-Type: application/json" \
      -H "Authorization: Bearer $SCIPHI_API_KEY" \
      -d '{
         "model": "SciPhi/Sensei-7B-V1",
         "prompt": "### Instruction: ...",
         "temperature": 0.0
       }'

**Response**:

.. code-block:: json

    {
        "id": "cmpl-f03f53c15a174ffe89bdfc83507de7a9",
        "object": "text_completion",
        "created": 389200,
        "model": "SciPhi/Sensei-7B-V1",
        "choices": [
            {
                "text": "The quest for the meaning of life is a profound...",
                "finish_reason": "length"
            }
        ],
        "usage": {
            "prompt_tokens": 49,
            "completion_tokens": 16
        }
    }

API Key and Signup
------------------

To access the SciPhi API, an API key is required. Sign up for an API key `here <https://www.sciphi.ai/signup>`_. Include this key in the request headers as demonstrated in the examples.
