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

3. Execute a Search:

   .. code-block:: shell

      export SCIPHI_API_KEY=MY_SCIPHI_API_KEY
      python -m agent_search.scripts.run_search run --query="What is Fermat's last theorem?"

   .. code-block:: none

      1. URL: https://en.wikipedia.org/wiki/Fermat's_last_theorem (Score: 0.89)
      --------------------------------------------------
      Fermat's Last Theorem
      Text:
      The case p = 3 was first stated by Abu-Mahmud Khojandi (10th century), but his attempted proof of the theorem was incorrect.[62] In 1770, Leonhard Euler gave a proof of p = 3,[63] but his proof by infinite descent[64] contained a major gap.[65] However, since Euler himself had proved the lemma necessary to complete the proof in other work, he is generally credited with the first proof.[66] Independent proofs were published[67] by Kausler (1802),[37] Legendre (1823, 1830),[39][68] Calzolari (1855),[69] Gabriel Lamé (1865),[70] Peter Guthrie Tait (1872),[71] Günther (1878),[72][full citation needed] Gambioli (1901),[48] Krey (1909),[73][full citation needed] Rychlík (1910),[53] Stockhaus (1910),[74] Carmichael (1915),[75] Johannes van der Corput (1915),[76] Axel Thue (1917),[77][full citation needed] and Duarte (1944).[78] The case p = 5 was proved[79] independently by Legendre and Peter Gustav Lejeune Dirichlet around 1825.[80] Alternative proofs were developed[81] by Carl Friedrich Gauss (1875,
      ...

4. Generate a search RAG Response:

   .. code-block:: shell

      # For SciPhi `SearchAgent` with AgentSearch
      export SCIPHI_API_KEY=MY_SCIPHI_API_KEY
      python -m agent_search.scripts.run_rag run --query="What is Fermat's last theorem?"

      # For OpenAI `gpt-3.5-turbo` LLM generation
      export SCIPHI_API_KEY=MY_SCIPHI_API_KEY
      export OPENAI_API_KEY=MY_OPENAI_KEY
      python -m agent_search.scripts.run_rag run --query="What is Fermat's last theorem?" --llm_provider_name=openai --llm_model_name=gpt-3.5-turbo

   .. code-block:: none

      ...
      {'response': "\nFermat's Last Theorem is a landmark statement in number theory, asserting that for any integer value of n greater than 2, the equation \\(x^n + y^n = z^n\\) has no solutions in positive integers x, y, and z [1][2]. This theorem has intrigued mathematicians for centuries, with the initial claim made by Pierre de Fermat in the 17th century. Fermat himself provided proofs for the cases n=4 and n=3, and partial proofs for other smaller values of n [16]. However, it was not until the late 20th century that the theorem was fully proven for all values of n greater than 2, thanks to the work of mathematician Andrew Wiles [7].\n\nThe proof of Fermat's Last Theorem has had a profound impact on mathematics, leading to significant advancements in the field. It has been described as one of the most difficult problems in the history of mathematics, and its resolution marked a major milestone in the understanding of number theory [10]. The proof itself has been recognized with prestigious awards, including the 2016 Abel Prize for Andrew Wiles, highlighting its importance and the depth of mathematical thought required to solve it [7].\n\nIn summary, Fermat's Last Theorem is a fundamental result in number theory, confirming a conjecture that had stumped mathematicians for over three centuries. The theorem's proof not only resolved a long-standing mathematical mystery but also catalyzed new developments within the discipline [1][2][7][10].\n\n", 'other_queries': ["Historical impact of Fermat's Last Theorem", "Explanation of Andrew Wiles' proof", "Significance of Fermat's Last Theorem in modern mathematics", 'The role of the modularity conjecture in the proof', "Advancements in number theory post-Fermat's Last Theorem"], ...SEARCH_RESULTS...}

5. Code your own search &/or RAG workflow:

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
