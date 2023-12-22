.. _agent_search_quick_start:

=====================================
 Quick Start Index for AgentSearch [ΨΦ]
=====================================

Introduction
------------

Installation and Setup
----------------------

1. **Install AgentSearch Client**

   .. code-block:: shell

      pip install agent-search

2. **API Key Registration**

   - Obtain a free API key from `SciPhi <https://www.sciphi.ai/signup>`_.

3. **Optional - Local Server Requirements**

   - Ensure Docker and Postgres are installed:
     - `Docker <https://www.docker.com/>`_
     - `Postgres <https://www.postgresql.org/download/>`_

Using AgentSearch
-----------------

1. **Perform a Search**

   .. code-block:: shell

      export SCIPHI_API_KEY=MY_SCIPHI_API_KEY
      python -m agent_search.scripts.run_search run --query="Your Search Query"

2. **Generate a RAG Response**

   .. code-block:: shell

      export SCIPHI_API_KEY=MY_SCIPHI_API_KEY
      export OPENAI_API_KEY=MY_OPENAI_KEY
      python -m agent_search.scripts.run_rag run --query="Your Search Query" --llm_provider_name=openai --llm_model_name=gpt-3.5-turbo

Local Setup and Initialization
------------------------------

1. **Launch Postgres Database**

   .. code-block:: shell

      sudo service postgresql start

2. **Populate Postgres Database**

   .. code-block:: shell

      python -m agent_search.scripts.populate_postgres_from_hf run

3. **Start Qdrant Service with Docker**

   .. code-block:: shell

      docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant

4. **Populate Vector Database (Qdrant)**

   .. code-block:: shell

      python -m agent_search.scripts.populate_qdrant_from_postgres run --delete_existing=True

5. **Run the Server**

   .. code-block:: shell

      python -m agent_search.app.server

Additional Notes
----------------

- Execute all commands from the root directory of the AgentSearch project.
- Customize the `query` parameter to suit your search requirements.

Documentation Links
-------------------

- `Installation Guide <installation>`_ (adjust if it's in a different location)
- `Quick Start Tutorial <quick_start>`_
- `API Documentation <../api/main>`_
