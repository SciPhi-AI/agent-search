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
      # Use the SciPhi `SearchAgent` for LLM RAG w/ AgentSearch
      python -m agent_search.scripts.run_rag run --query="What is Fermat's last theorem?"
      # ... Output ...
      # {"summary": "\nFermat's Last Theorem is a significant result in number theory, stating that for any natural number n greater than 2, there are no solutions to the equation \\(a^n + b^n = c^n\\) where \\(a\\), \\(b\\), and \\(c\\) are positive integers [5]. The theorem was first proposed by Pierre de Fermat in the margins of his copy of Diophantus's \"Arithmetica\" in the 17th century, but it remained unproved for over three centuries [8]. The first case of the theorem to be proven was by Fermat himself for \\(n = 4\\), using a method of infinite descent [9]. Leonhard Euler later provided a proof for the case \\(n = 3\\), although his initial proof contained errors that were later corrected [9].\n\nThe theorem was finally proven in its entirety in 1995 by British mathematician Andrew Wiles, using sophisticated mathematical tools and techniques that were not available during Fermat's lifetime [10]. This breakthrough marked the end of a long period of mathematical speculation and the resolution of a major historical puzzle in mathematics [10]. The proof of Fermat's Last Theorem has been hailed as one of the most significant achievements in the history of mathematics, demonstrating the power of modern mathematical methods and the persistence of mathematical inquiry over centuries [10].\n\n", "other_queries": ["Details of Fermat's Last Theorem proof", "Historical impact of Fermat's Last Theorem", "Contributions of Andrew Wiles to mathematics", "Techniques used in the proof of Fermat's Last Theorem", "Evolution of number theory post-Fermat's Last Theorem"]}</s>

      export SCIPHI_API_KEY=MY_SCIPHI_API_KEY
      export OPENAI_API_KEY=MY_OPENAI_KEY
      # Use OpenAI `gpt-3.5-turbo` for LLM generation
      python -m agent_search.scripts.run_rag run --query="What is Fermat's last theorem?" --llm_provider_name=openai --llm_model_name=gpt-3.5-turbo

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

- `Installation Guide <installation.html>`_ 
- `Quick Start Tutorial <quick_start.html>`_
- `API Documentation <../api/main.html>`_
