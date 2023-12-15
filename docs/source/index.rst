Welcome to AgentSearch [ΨΦ]
===========================

.. image:: https://github.com/SciPhi-AI/agent-search/assets/68796651/56268e41-130f-4d2f-ba22-b565f7642713
   :width: 716
   :alt: AgentSearch Banner
   :align: center

.. raw:: html

   <p style="text-align:center">
   <strong>AI's Knowledge Engine.
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

3. Run a query:

  .. code-block:: shell

     SCIPHI_API_KEY=$SCIPHI_API_KEY python -m agent_search.scripts.run_query query --query="What is Fermat's last theorem?"

     # For self-hosted local instances, follow the local setup steps below.

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

- Ensure all commands are executed from the root directory of the AgentSearch project.
- Customize the `query` in the command to fit your search needs.

Citing Our Work
---------------

.. code-block:: none

   @software{AgentSearch,
      author = {Colegrove, Owen},
      doi = {Pending},
      month = {09},
      title = {{AgentSearch: An agent-first search engine.}},
      url = {https://github.com/SciPhi-AI/agent-search},
      year = {2023}
   }

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
