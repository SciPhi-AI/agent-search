# AgentSearch [ΨΦ]: A powerful search agent client and search engine.

![AgentSearch Banner](https://github.com/SciPhi-AI/agent-search/assets/68796651/56268e41-130f-4d2f-ba22-b565f7642713)

This framework facilitates seamless integration with the AgentSearch dataset or hosted search APIs (`e.g. Search Engines`) and with RAG-specialized LLM's (`e.g. Search Agents`).

## Features of AgentSearch
- **Search Agent**: Seamless integration with any RAG-specialized LLM, such as [Sensei-7B](https://huggingface.co/SciPhi/Sensei-7B-V1).
- **Customizable Search**: Deploy your own local search engine with the [AgentSearch dataset](https://huggingface.co/datasets/SciPhi/AgentSearch-V1). Or, introduce your own custom datasets to meet your specific needs.
- **API Endpoint**: Connect with SciPhi and other search provider APIs for easy deployment.

## Quickstart Guide for AgentSearch

### Install the AgentSearch Client


```shell
pip install agent-search

# Get a free API key at https://www.sciphi.ai/signup
export SCIPHI_API_KEY=$MY_SCIPHI_API_KEY
```


```python
# Requires SCIPHI_API_KEY in env
from agent_search import SciPhi

client = SciPhi()

# Perform a search
search_response = client.search(query='Quantum Field Theory', search_provider='agent-search')
print(search_response)
# [{ 'score': '.89', 'url': 'https://...', 'metadata': {...} }

# Generate a RAG response
rag_response = client.get_search_rag_response(query='latest news', search_provider='bing', llm_model='SciPhi/Sensei-7B-V1')
print(rag_response)
# { 'response': '...', 'other_queries': '...', 'search_results': '...' }
```
---

### Community & Support

- Engage with the community on [Discord](https://discord.gg/j9GxfbxqAe).
- For tailored inquiries or feedback, please [email us](mailto:owen@sciphi.ai).

### Local AgentSearch Setup and Initialization

For self-hosting, follow the steps below.

#### Prerequisites

Ensure Docker and Postgres are installed on your system. 
- [Download Docker here](https://www.docker.com/).
- [Download Postgres here](https://www.postgresql.org/download/).

#### Steps:

1. **Launch Postgres Database**:
   - Start the Postgres service on your system:
     ```shell
     # Command to start Postgres, adjust based on your system's configuration
     sudo service postgresql start
     ```
   - This step ensures that the Postgres database is running and ready to be populated.

2. **Relational Database Population**:
   - Command to populate the Postgres database:
     ```shell
     python -m agent_search.scripts.populate_postgres_from_hf run
     ```
   - This script populates a postgres database with the parameters from `config.ini`, adaptable to custom datasets. For help directly istalling the full 4TB postgres database, contact [our team](mailto:owen@sciphi.ai).

3. **Start Qdrant Service with Docker**:
   - Run the Qdrant service in Docker:
     ```shell
     docker run -p 6333:6333 -p 6334:6334 \
         -v $(pwd)/qdrant_storage:/qdrant/storage:z \
         qdrant/qdrant
     ```
   - For Qdrant installation guidance, see [Qdrant Documentation](https://qdrant.tech/documentation/quick-start/).

4. **Vector Database Population**:
   - Populate the Vector database:
     ```shell
     python -m agent_search.scripts.populate_qdrant_from_postgres run --delete_existing=True
     ```
   - This step prepares a qdrant database with the parameters from `config.ini`. For direct installation assistance, contact [our team](mailto:owen@sciphi.ai).

5. **Run the Server**:
   - Launch the AgentSearch server:
     ```shell
     python -m agent_search.app.server
     ```

### Additional Notes

- Execute all commands from the root directory of the AgentSearch project.
- Replace `query` in the run command with your search query.
- Check back soon for our User Guide. 
<!-- [User Guide](link-to-user-guide). -->