Welcome to AgentSearch [ΨΦ]
===========================

.. image:: https://github.com/SciPhi-AI/agent-search/assets/68796651/56268e41-130f-4d2f-ba22-b565f7642713
   :width: 716
   :alt: AgentSearch Banner
   :align: center

.. raw:: html

   <p style="text-align:center">
   </p>

   <p style="text-align:center">
   <script async defer src="https://buttons.github.io/buttons.js"></script>
   <a class="github-button" href="https://github.com/SciPhi-AI/agent-search" data-show-count="true" data-size="large" aria-label="Star">Star</a>
   <a class="github-button" href="https://github.com/SciPhi-AI/agent-search/subscription" data-icon="octicon-eye" data-size="large" aria-label="Watch">Watch</a>
   <a class="github-button" href="https://github.com/SciPhi-AI/agent-search/fork" data-icon="octicon-repo-forked" data-size="large" aria-label="Fork">Fork</a>
   </p>

This framework facilitates seamless integration with the AgentSearch dataset or hosted search APIs (e.g., Search Engines) and with RAG-specialized LLMs (e.g., Search Agents).

Features of AgentSearch
-----------------------

- **Search Agent**: Seamless integration with any RAG-specialized LLM, such as `Sensei-7B <https://huggingface.co/SciPhi/Sensei-7B-V1>`_.
- **Customizable Search**: Deploy your own local search engine with the `AgentSearch dataset <https://huggingface.co/datasets/SciPhi/AgentSearch-V1>`_. Or, introduce your own custom datasets to meet your specific needs.
- **API Endpoint**: Connect with SciPhi and other search provider APIs for easy deployment.

Quickstart Guide for AgentSearch
--------------------------------

Quick Setup
+++++++++++

1. Install the AgentSearch client:

   .. code-block:: shell

      pip install agent-search

2. Obtain a free API key from SciPhi:

   `SciPhi API Key Signup <https://www.sciphi.ai/signup>`_

3. Code your own search &/or RAG workflow:

   .. code-block:: python

      # Requires SCIPHI_API_KEY in the environment
      from agent_search import SciPhi

      # Perform a search
      search_response = client.search(query='Quantum Field Theory', search_provider='agent-search')
      print(search_response)
      # [{ 'score': '.89', 'url': 'https://...', 'metadata': {...} }

      # Generate a RAG response
      rag_response = client.get_search_rag_response(query='latest news', search_provider='bing', llm_model='SciPhi/Sensei-7B-V1')
      print(rag_response)
      # { 'response': '...', 'other_queries': '...', 'search_results': '...' }


Local Setup and Initialization
-------------------------------
Interested in standing up an instance of the open source search dataset that pairs with AgentSearch locally? Then follow the guide below.

.. warning::
   This setup documentation is preliminary and not yet finalized. Please note that the setup process may change in the future.

Prerequisites
+++++++++++++

Ensure Docker and Postgres are installed:

- Docker: `Download from Docker's official website <https://www.docker.com/>`.
- Postgres: `Download from PostgreSQL's official website <https://www.postgresql.org/download/>`.

1. **Launch Postgres Database**:

   .. code-block:: shell

      sudo service postgresql start

2. **Populate Relational Database (Postgres)**:

   .. code-block:: shell

      python -m agent_search.scripts.populate_postgres_from_hf run

3. **Start Qdrant Service with Docker**:

   .. code-block:: shell

      docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant

4. **Populate Vector Database (Qdrant)**:

   .. code-block:: shell

      python -m agent_search.scripts.populate_qdrant_from_postgres run --delete_existing=True

5. **Run the Server**:

   .. code-block:: shell

      python -m agent_search.app.server


Additional Notes
----------------

- Ensure all installation commands are executed from the root directory of the AgentSearch project.

Documentation
-------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   setup/installation
   setup/quick_start

.. toctree::
   :maxdepth: 2
   :caption: API

   api/main
   python_client/main
