---

# AgentSearch: Advanced RAG-specialized LLM & Search Engine Integration Framework

![AgentSearch Banner](https://github.com/SciPhi-AI/agent-search/assets/68796651/56268e41-130f-4d2f-ba22-b565f7642713)

## Overview

AgentSearch is a groundbreaking framework designed for efficient and seamless integration with the AgentSearch dataset and various hosted search APIs, including popular search engines. It specializes in working with RAG (Retrieval-Augmented Generation) specialized Language Learning Models (LLMs) like Sensei-7B, enhancing the capabilities of search agents in diverse applications.

### Key Features

- **Search Agent Integration:** Effortlessly connect with any RAG-specialized LLM, including the cutting-edge Sensei-7B model.
- **Customizable Search Solutions:** Utilize the AgentSearch dataset for deploying your local search engine or incorporate custom datasets for tailored search functionalities.
- **API Connectivity:** Easily integrate with leading search provider APIs such as SciPhi for streamlined deployment.

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

Import and use the AgentSearch client in your project:

```python
from agent_search import SciPhi

client = SciPhi()

# Perform a search
search_response = client.search(query='Quantum Field Theory', search_provider='agent-search')
print(search_response)
# [{ 'score': '.89', 'url': 'https://...', 'metadata': {...} }]

# Generate a RAG response
rag_response = client.get_search_rag_response(query='latest news', search_provider='bing', llm_model='SciPhi/Sensei-7B-V1')
print(rag_response)
# { 'response': '...', 'other_queries': '...', 'search_results': '...' }
```

## Community & Support

- **Engage with Us:** Join our [Discord community](#) for discussions and updates.
- **Feedback & Inquiries:** Contact us via email for personalized support.

## Self-Hosting Guide

AgentSearch is a multi-TB dataset hosted on [here on HuggingFace](https://huggingface.co/datasets/SciPhi/AgentSearch-V1). This repository has the necessary code for individuals to download and host their own search engine with this dataset.

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
   python -m agent_search.scripts.populate_postgres_from_hf run
   ```
3. **Qdrant Service with Docker**
   ```bash
   docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant
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

---
