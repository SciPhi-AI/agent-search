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

- **Customizable**: Upload local data or adapt provided datasets to meet specific requirements.
- **Offline Support**: Operates in a completely offline environment.
- **API Endpoint**: Offers fully managed access through a dedicated API for seamless integration into various workflows.

Quickstart Guide for AgentSearch
--------------------------------

Quick Setup
+++++++++++

1. Install the AgentSearch client:

   .. code-block:: shell

      pip install agent-search

2. Obtain a free API key from SciPhi:

   `SciPhi API Key Signup <https://www.sciphi.ai/signup>`_

3. Perform a Search:

   .. code-block:: shell

      export SCIPHI_API_KEY=MY_SCIPHI_API_KEY
      python -m agent_search.scripts.run_search run --query="What is Fermat's last theorem?"

4. Generate a RAG Response:

   .. code-block:: shell

      export SCIPHI_API_KEY=MY_SCIPHI_API_KEY
      # Use the SciPhi `SearchAgent` for LLM RAG w/ AgentSearch
      python -m agent_search.scripts.run_rag run --query="What is Fermat's last theorem?"
      # ... Output ...
      # {"summary": "\nFermat's Last Theorem is a significant result in number theory, stating that for any natural number n greater than 2, there are no solutions to the equation \\(a^n + b^n = c^n\\) where \\(a\\), \\(b\\), and \\(c\\) are positive integers [5]. The theorem was first proposed by Pierre de Fermat in the margins of his copy of Diophantus's \"Arithmetica\" in the 17th century, but it remained unproved for over three centuries [8]. The first case of the theorem to be proven was by Fermat himself for \\(n = 4\\), using a method of infinite descent [9]. Leonhard Euler later provided a proof for the case \\(n = 3\\), although his initial proof contained errors that were later corrected [9].\n\nThe theorem was finally proven in its entirety in 1995 by British mathematician Andrew Wiles, using sophisticated mathematical tools and techniques that were not available during Fermat's lifetime [10]. This breakthrough marked the end of a long period of mathematical speculation and the resolution of a major historical puzzle in mathematics [10]. The proof of Fermat's Last Theorem has been hailed as one of the most significant achievements in the history of mathematics, demonstrating the power of modern mathematical methods and the persistence of mathematical inquiry over centuries [10].\n\n", "other_queries": ["Details of Fermat's Last Theorem proof", "Historical impact of Fermat's Last Theorem", "Contributions of Andrew Wiles to mathematics", "Techniques used in the proof of Fermat's Last Theorem", "Evolution of number theory post-Fermat's Last Theorem"]}</s>

      export SCIPHI_API_KEY=MY_SCIPHI_API_KEY
      export OPENAI_API_KEY=MY_OPENAI_KEY
      # Use OpenAI `gpt-3.5-turbo` for LLM generation
      python -m agent_search.scripts.run_rag run --query="What is Fermat's last theorem?" --llm_provider_name=openai --llm_model_name=gpt-3.5-turbo

Example Outputs from Queries
-------------------------------

- Standard Search Output:

.. code-block:: none

   1. URL: https://en.wikipedia.org/wiki/Wiles%27s%20proof%20of%20Fermat%27s%20Last%20Theorem (Score: 0.85)
   --------------------------------------------------
   Title: Wiles's proof of Fermat's Last Theorem
   Text:
   is a proof by British mathematician Andrew Wiles of a special case of the modularity theorem for elliptic curves... Output Continues ...

- RAG Response Output:

.. code-block:: none

   {"summary": "\nFermat's Last Theorem is a significant result in number theory, stating that for any natural number n greater than 2, there are no solutions to the equation \\(a^n + b^n = c^n\\) where \\(a\\), \\(b\\), and \\(c\\) are positive integers [5]. The theorem was first proposed by Pierre de Fermat in the margins of his copy of Diophantus's \"Arithmetica\" in the 17th century, but it remained unproved for over three centuries [8]. The first case of the theorem to be proven was by Fermat himself for \\(n = 4\\), using a method of infinite descent [9]. Leonhard Euler later provided a proof for the case \\(n = 3\\), although his initial proof contained errors that were later corrected [9].\n\nThe theorem was finally proven in its entirety in 1995 by British mathematician Andrew Wiles, using sophisticated mathematical tools and techniques that were not available during Fermat's lifetime [10]. This breakthrough marked the end of a long period of mathematical speculation and the resolution of a major historical puzzle in mathematics [10]. The proof of Fermat's Last Theorem has been hailed as one of the most significant achievements in the history of mathematics, demonstrating the power of modern mathematical methods and the persistence of mathematical inquiry over centuries [10].\n\n", "other_queries": ["Details of Fermat's Last Theorem proof", "Historical impact of Fermat's Last Theorem", "Contributions of Andrew Wiles to mathematics", "Techniques used in the proof of Fermat's Last Theorem", "Evolution of number theory post-Fermat's Last Theorem"]}

Local Setup and Initialization
-------------------------------

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
- Customize the `query` in the command to fit your search needs.

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
