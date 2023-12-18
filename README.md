# AgentSearch [ΨΦ]: A Comprehensive Agent-First Framework and Dataset for Webscale Search

![AgentSearch Banner](https://github.com/SciPhi-AI/agent-search/assets/68796651/56268e41-130f-4d2f-ba22-b565f7642713)

AgentSearch is a powerful agent-first search engine which enables you to run a webscale search engine locally or to connect via remote API. It's ideal for both Large Language Models (LLMs) and human users, providing access to over one billion high-quality embeddings from diverse sources like Creative Commons, Arxiv, Wikipedia, and Project Gutenberg.

## Features of AgentSearch

- **Customizable**: Allows uploading of local data or tailoring of provided datasets to meet specific needs.
- **Offline Support**: Facilitates operation in a completely offline environment. Download the full [dataset here](https://huggingface.co/datasets/SciPhi/AgentSearch-V1).
- **API Endpoint**: Offers fully managed access through a dedicated API for seamless integration into various workflows.

## Quickstart Guide for AgentSearch

### Install the AgentSearch Client

```shell
pip install agent-search
```

### Perform a Search

- To perform a search with the hosted AgentSearch API, follow these steps:

1. Register for a free API key at [SciPhi](https://www.sciphi.ai/).
2. Use the following command to run a search query:

```shell
   export SCIPHI_API_KEY=MY_SCIPHI_API_KEY
   python -m agent_search.scripts.run_search run --query="What is Fermat's last theorem?"
```

This will output results like the following:

```output
1. URL: https://en.wikipedia.org/wiki/Wiles%27s%20proof%20of%20Fermat%27s%20Last%20Theorem (Score: 0.85)
--------------------------------------------------
Title: Wiles's proof of Fermat's Last Theorem
Text:
is a proof by British mathematician Andrew Wiles of a special case of the modularity theorem for elliptic curves ... Response Continues ...
```

For further information, you may refer to the [documentation](https://agent-search.readthedocs.io/en/latest/).

### Generate a RAG response

- To generate a rag response with the hosted AgentSearch API:

```shell
# Install SciPhi's synthesizer package -
pip install sciphi-synthesizer

# Setup environment
export SCIPHI_API_KEY=MY_SCIPHI_API_KEY
# Use the SciPhi `SearchAgent` for LLM RAG w/ AgentSearch
python -m agent_search.scripts.run_rag run --query="What is Fermat's last theorem?"

export OPENAI_API_KEY=MY_OPENAI_KEY
# Use OpenAI `gpt-3.5-turbo` for LLM generation
python -m agent_search.scripts.run_rag run --query="What is Fermat's last theorem?" --llm_provider_name=openai --llm_model_name=gpt-3.5-turbo
```

Resulting output:

```output
Fermat's Last Theorem was proven by British mathematician Andrew Wiles in 1994 (Wikipedia). Wiles's proof was based ...
```

---

### Community & Support

- Engage with the community on [Discord](https://discord.gg/j9GxfbxqAe).
- For tailored inquiries or feedback, please [email us](mailto:owen@sciphi.ai).

### Local Setup and Initialization

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