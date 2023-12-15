Welcome to AgentSearch [ΨΦ]
===========================

.. image:: https://github.com/SciPhi-AI/agent-search/assets/68796651/56268e41-130f-4d2f-ba22-b565f7642713
   :width: 716
   :alt: AgentSearch Banner
   :align: center

.. raw:: html

   <p style="text-align:center">
   <strong>An agent-first search engine.
   </strong>
   </p>

   <p style="text-align:center">
   <script async defer src="https://buttons.github.io/buttons.js"></script>
   <a class="github-button" href="https://github.com/SciPhi-AI/agent-search" data-show-count="true" data-size="large" aria-label="Star">Star</a>
   <a class="github-button" href="https://github.com/SciPhi-AI/agent-search/subscription" data-icon="octicon-eye" data-size="large" aria-label="Watch">Watch</a>
   <a class="github-button" href="https://github.com/SciPhi-AI/agent-search/fork" data-icon="octicon-repo-forked" data-size="large" aria-label="Fork">Fork</a>
   </p>

AgentSearch [ΨΦ]: A Comprehensive Agent-First Framework and Dataset for Webscale Search
----------------------------------------------------------------------------------------

AgentSearch is a powerful new tool that allows you to operate a webscale search engine locally, catering to both Large Language Models (LLMs) and human users. This open-source initiative provides access to over one billion high-quality embeddings sourced from a wide array of content, including selectively filtered Creative Commons data and the entirety of Arxiv, Wikipedia, and Project Gutenberg.

Features of AgentSearch
------------------------

- **Gated Access**: Controlled and secure access to the search engine, ensuring data integrity and privacy.
- **Offline Support**: Ability to operate in a fully offline environment.
- **Customizable**: Upload your own local data or tailor the provided datasets according to your needs.
- **API Endpoint**: Fully managed access through a dedicated API, facilitating easy and efficient integration into various workflows.

Quickstart Guide for AgentSearch
--------------------------------

Quick Setup
+++++++++++

1. Install the AgentSearch package:

   .. code-block:: shell

      pip install agent-search

2. Register at `AgentSearch Signup <https://www.sciphi.ai/signup>`_ for a free API key.

3. Run a search:

  .. code-block:: shell

     SCIPHI_API_KEY=$SCIPHI_API_KEY python -m agent_search.scripts.run_search run --query="What is Fermat's last theorem?"

     # For self-hosted local instances, follow the local setup steps below.


4. Create a RAG grounded response:

  .. code-block:: shell

     SCIPHI_API_KEY=$SCIPHI_API_KEY OPENAI_API_KEY=$OPENAI_API_KEY python -m agent_search.scripts.run_rag run --query="What is Fermat's last theorem?" --llm_provider_name=openai --llm_model_name=gpt-3.5-turbo

     # For self-hosted local instances, follow the local setup steps below.     

Example Outputs from Queries
-------------------------------

- Standard Search Output:

  ```output
  1. URL: https://en.wikipedia.org/wiki/Wiles%27s%20proof%20of%20Fermat%27s%20Last%20Theorem (Score: 0.85)
  --------------------------------------------------
  Title: Wiles's proof of Fermat's Last Theorem
  Text:
  is a proof by British mathematician Andrew Wiles of a special case of the modularity theorem for elliptic curves. Together with Ribet's theorem, it provides a proof for Fermat's Last Theorem. Both Fermat's Last Theorem and the modularity theorem were almost universally considered inaccessible to proof by contemporaneous mathematicians, meaning that they were believed to be impossible to prove using current knowledge.
  ...
  ```

- RAG Grounded Response Output:

  ```output
  ...
  Fermat's Last Theorem was proven by British mathematician Andrew Wiles in 1994 (Wikipedia). Wiles's proof was based ...
  ```

Local Setup and Initialization
-------------------------------

Prerequisites
+++++++++++++

Ensure Docker and Postgres are installed on your system. 
- For Docker: `Download from Docker's official website <https://www.docker.com/>`.
- For Postgres: `Download from PostgreSQL's official website <https://www.postgresql.org/download/>`.

1. **Launch Postgres Database**:

   Start the Postgres service on your system:

   .. code-block:: shell

      # Command to start Postgres, adjust based on your system's configuration
      sudo service postgresql start

   Ensure that the Postgres database is running and ready for data population.

2. **Relational (Postgres) Database Population**:

   Populate your Postgres database using:

   .. code-block:: shell

      python -m agent_search.scripts.populate_dbs populate_postgres_from_hf run

   This script sets up and populates the Postgres database defined in `config.ini`.

3. **Start Qdrant Service with Docker**:

   Run Qdrant in a Docker container:

   .. code-block:: shell

      docker run -p 6333:6333 -p 6334:6334 \
          -v $(pwd)/qdrant_storage:/qdrant/storage:z \
          qdrant/qdrant

   For more details on Qdrant installation, refer to `Qdrant Documentation <https://qdrant.tech/documentation/quick-start/>`.

4. **Vector (Qdrant) Database Population**:

   Populate the Vector database:

   .. code-block:: shell

      python -m agent_search.scripts.populate_dbs populate_qdrant_from_postgres run --delete_existing=True

   This script sets up and populates the Qdrant vector database as per `config.ini`.

5. **Run the Server**:

   Launch the AgentSearch server:

   .. code-block:: shell

      python -m agent_search.app.server.py

Additional Notes
----------------

- Ensure all installation commands are executed from the root directory of the AgentSearch project.
- Customize the `query` in the command to fit your search needs.

Documentation
-------------

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   setup/installation

.. toctree::
   :maxdepth: 1
   :caption: API

   api/main
