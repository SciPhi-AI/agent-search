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


AgentSearch is a framework for powering search agents by seamlessly integrating LLM technologies from various providers with different search engines. This integration enables search agents to perform a wide range of functions through Retrieval-Augmented Generation (RAG), including summarizing search results, generating new queries, and retrieving detailed downstream results.

Features of AgentSearch
-----------------------

- **Search Agent Integration**: Effortlessly build a search agent by connecting any search-specialized LLM, such as `Sensei-7B <https://huggingface.co/SciPhi/Sensei-7B-V1>`_, with a supported search engine.
- **Customizable Search**: Utilize the `AgentSearch dataset <https://huggingface.co/datasets/SciPhi/AgentSearch-V1>` in conjunction with this framework to deploy a customizable local search engine.
- **API Endpoint Integration**: Seamlessly integrate with a variety of hosted provider APIs for diverse search solutions, including Bing, SERP API, and AgentSearch. Additionally, support is provided for LLMs from SciPhi, HuggingFace, OpenAI, Anthropic, and more.

Quickstart Guide for AgentSearch
--------------------------------

1. Install the AgentSearch client:

   .. code-block:: shell

      pip install agent-search

2. Obtain a free API key from SciPhi:

   `SciPhi API Key Signup <https://www.sciphi.ai/signup>`_

3. Call a pre-configured search agent endpoint:

   .. code-block:: python

      # Requires SCIPHI_API_KEY in the environment
      from agent_search import SciPhi

      client = SciPhi()

      # Search, then summarize result and generate related queries
      agent_summary = client.get_search_rag_response(query='latest news', search_provider='bing', llm_model='SciPhi/Sensei-7B-V1')
      print(agent_summary)
      # {'response': "The latest news encompasses ... and its consequences [2].", 'related_queries': ['Details on the...', ...], 'search_results' : [...]}

4. Standalone searches and from the AgentSearch search engine are supported:

   .. code-block:: python
      
      from agent_search import SciPhi

      client = SciPhi()

      # Perform a search
      search_response = client.search(query='Quantum Field Theory', search_provider='agent-search')

      print(search_response)
      # [{ 'score': '.89', 'url': 'https://...', 'metadata': {...} }

5. Code your own custom search agent workflow:

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

Additional Notes
----------------

- Ensure all installation commands are executed from the root directory of the AgentSearch project.
- For support, join the `Discord community <https://discord.gg/mN4kWbsgRu>`

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
