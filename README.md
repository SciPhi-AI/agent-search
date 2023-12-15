# AgentSearch [ΨΦ]: A Comprehensive Agent-First Framework and Dataset for Webscale Search

![AgentSearch Banner](https://github.com/SciPhi-AI/agent-search/assets/68796651/56268e41-130f-4d2f-ba22-b565f7642713)

AgentSearch is a powerful new tool designed for data scientists, developers, and researchers, allowing you to operate a webscale search engine locally. It's ideal for both Large Language Models (LLMs) and human users, providing access to over one billion high-quality embeddings from diverse sources like Creative Commons, Arxiv, Wikipedia, and Project Gutenberg.

## Features of AgentSearch

- **Gated Access**: Ensures controlled and secure access to the search engine, maintaining data integrity and privacy.
- **Offline Support**: Facilitates operation in a completely offline environment.
- **Customizable**: Allows uploading of local data or tailoring of provided datasets to meet specific needs.
- **API Endpoint**: Offers fully managed access through a dedicated API for seamless integration into various workflows.

## Quickstart Guide for AgentSearch

### Install the AgentSearch Client

```shell
pip install agent-search
```

### Perform a Search

- To perform a search with the hosted AgentSearch API:

```shell
SCIPHI_API_KEY=$SCIPHI_API_KEY python -m agent_search.scripts.run_search run --query="What is Fermat's last theorem?"
```

Register first for a free API key with [SciPhi](https://www.sciphi.ai/). For further information, you may refer to the [documentation](https://agent-search.readthedocs.io/en/latest/).

```output
INFO:root:1. URL: https://en.wikipedia.org/wiki/Wiles%27s%20proof%20of%20Fermat%27s%20Last%20Theorem (Score: 0.85)
INFO:root:--------------------------------------------------
INFO:root:Title: Wiles's proof of Fermat's Last Theorem
INFO:root:Text:
is a proof by British mathematician Andrew Wiles of a special case of the modularity theorem for elliptic curves. Together with Ribet's theorem, it provides a proof for Fermat's Last Theorem. Both Fermat's Last Theorem and the modularity theorem were almost universally considered inaccessible to proof by contemporaneous mathematicians, meaning that they were believed to be impossible to prove using current knowledge.
...
```

### Generate a RAG response

- To perform a search with the hosted AgentSearch API:

```shell
SCIPHI_API_KEY=$SCIPHI_API_KEY OPENAI_API_KEY=$OPENAI_API_KEY python -m agent_search.scripts.run_rag run --query="What is Fermat's last theorem?" --llm_provider_name=openai --llm_model_name=gpt-3.5-turbo
```

```output
...
Fermat's Last Theorem was proven by British mathematician Andrew Wiles in 1994 (Wikipedia). Wiles's proof was based ...
```

Register first for a free API key with [SciPhi](https://www.sciphi.ai/). For further information, you may refer to the [documentation](https://agent-search.readthedocs.io/en/latest/).

---


### Local Setup and Initialization

For self-hosting, follow the steps below.

#### Prerequisites

Ensure Docker and Postgres are installed on your system. 
- [Download Docker here](https://www.docker.com/).
- [Download Postgres here](https://www.postgresql.org/download/).

This addition provides users with direct links to download both Docker and Postgres, ensuring they have the necessary tools to proceed with the AgentSearch setup.
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
   - This script populates the database defined in `config.ini`, adaptable to custom datasets. For assistance with the 4TB postgres database installation, contact [our team](mailto:owen@sciphi.ai).

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
   - This step prepares the qdrant vector database as described in `config.ini`. For direct installation assistance, contact [our team](mailto:owen@sciphi.ai).

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

## Troubleshooting and FAQs

Encounter an issue? Check our [FAQs](link-to-faqs) or visit our [community forum](link-to-forum) for support.

## Version Information

Currently running AgentSearch version: 0.0.2.