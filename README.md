# AgentSearch: A framework for powering search agents and enabling customizable local search.

![AgentSearch Banner](https://github.com/SciPhi-AI/agent-search/assets/68796651/8d0424e6-84e3-42f6-9893-3d63f9b2a58d)

AgentSearch is a framework for powering search agents by seamlessly integrating LLM technologies from various providers with different search engines. This integration enables search agents to perform a wide range of functions through Retrieval-Augmented Generation (RAG), including summarizing search results, generating new queries, and retrieving detailed downstream results.

## Features of AgentSearch

- **Search Agent Integration**: Effortlessly build a search agent by connecting any search-specialized LLM, such as [Sensei-7B](https://huggingface.co/SciPhi/Sensei-7B-V1), with a supported search engine.
- **Customizable Search**: Utilize the [AgentSearch dataset](https://huggingface.co/datasets/SciPhi/AgentSearch-V1) in conjunction with this framework to deploy a customizable local search engine.
- **API Endpoint Integration**: Seamlessly integrate with a variety of hosted provider APIs for diverse search solutions, offering ease of use and flexibility, including Bing, SERP API, and AgentSearch. Additionally, support is provided for LLMs from SciPhi, HuggingFace, OpenAI, Anthropic, and more.

## Quickstart Guide

### Installation

```bash
pip install agent-search
```

### Configuration

Get your free API key from [SciPhi](https://www.sciphi.ai/signup) and set it in your environment:

```bash
export SCIPHI_API_KEY=$MY_SCIPHI_API_KEY
```

### Usage

Code your own search agent workflow:


```python
from agent_search import SciPhi

client = SciPhi()

# Search, then summarize result and generate related queries
agent_summary = client.get_search_rag_response(query='latest news', search_provider='bing', llm_model='SciPhi/Sensei-7B-V1')
print(agent_summary)
# { 'response': '...', 'other_queries': '...', 'search_results': '...' }
```

Standalone searches and from the AgentSearch search engine are supported:

```python

from agent_search import SciPhi

client = SciPhi()

# Perform a search
search_response = client.search(query='Quantum Field Theory', search_provider='agent-search')

print(search_response)
# [{ 'score': '.89', 'url': 'https://...', 'metadata': {...} }]
```

Get a raw completion from the SciPhi API endpoint:
```python

from agent_search import SciPhi

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

# hack to get a JSON response (we are working to improve this)
json_response_prefix = '{"summary":'

# Prepare a prompt
formatted_prompt = f"### Instruction:{instruction}\n\nQuery:\n{query}\n\nSearch Results:\n${search_context}\n\nQuery:\n{query}\n### Response:\n{json_response_prefix}",

# Generate a completion with Sensei-7B-V1
completion = json_response_prefix + client.completion(formatted_prompt, llm_model_name="SciPhi/Sensei-7B-V1")

print(completion)
# {
#   "summary":  "\nFermat's Last Theorem is a mathematical proposition first prop ... ",
#   "other_queries": ["The role of elliptic curves in the proof of Fermat's Last Theorem", ...]
# }
```

## Community & Support

- **Engage with Us:** Join our [Discord community](#) for discussions and updates.
- **Feedback & Inquiries:** Contact us via email for personalized support.

## Self-Hosting Guide

AgentSearch is a multi-TB dataset curated by SciPhi and accessible [on HuggingFace](https://huggingface.co/datasets/SciPhi/AgentSearch-V1). This repository has the necessary code for individuals to download and host their own search engine with this dataset.

> **Warning:** This setup documentation is preliminary and not yet finalized. Please note that the setup process may change in the future.

### Prerequisites

- Docker: [Download here](#)
- Postgres: [Download here](#)

### Setup Steps

1. **Start Postgres Database**
   ```bash
   sudo service postgresql start
   ```
2. **Populate Database**
   ```bash
   # Needs revision. 
   # python -m agent_search.scripts.populate_postgres_from_hf run
   ```
3. **Qdrant Service with Docker**
   ```bash
   # Needs revision. 
   # docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
   ```
4. **Populate Vector Database**
   ```bash
   python -m agent_search.scripts.populate_qdrant_from_postgres run --delete_existing=True
   ```
5. **Launch Server**
   ```bash
   python -m agent_search.app.server
   ```

### Additional Notes

- Execute commands from the root directory of the AgentSearch project.
- Replace `query` in the run command with your specific search query.
- User Guide coming soon!
