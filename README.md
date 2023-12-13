# AgentSearch [ΨΦ]: A Comprehensive Agent-First Framework and Dataset for Webscale Search
![agent_search_banner](https://github.com/SciPhi-AI/agent-search/assets/68796651/56268e41-130f-4d2f-ba22-b565f7642713)

AgentSearch is a powerful new tool that allows you to operate a webscale search engine locally, catering to both Large Language Models (LLMs) and human users. This open-source initiative provides access to over one billion high-quality embeddings sourced from a wide array of content, including selectively filtered Creative Commons data and the entirety of Arxiv, Wikipedia, and Project Gutenberg.

## Features of AgentSearch

- **Gated Access**: Controlled and secure access to the search engine, ensuring data integrity and privacy.
- **Offline Support**: Ability to operate in a fully offline environment.
- **Customizable**: Upload your own local data or tailor the provided datasets according to your needs.
- **API Endpoint**: AgentSearch offers a fully managed access through a dedicated API, facilitating easy and efficient integration into various workflows.

## Quickstart Guide for AgentSearch

### Install the AgentSearch client

   ```shell
   pip install agent-search
   ```

### Run a Query

- To perform a search with the hosted AgentSearch API, use:

  ```shell
  SCIPHI_API_KEY=$SCIPHI_API_KEY python -m agent_search.script.run_query query --query="What is Fermat's last theorem?"
  ```

  Please register first for free API key at [AgentSearch](https://www.sciphi.ai/). If you prefer to self-host then follow the steps below to launch your local agent-first search engine.

### Local Setup and Initialization

#### Prerequisites

Make sure Docker is installed on your system. If not, download and install it from [Docker's official website](https://www.docker.com/).

1. **Database Population**:
   - Populate the SQLite database with this command:

     ```shell
     python -m agent_search.script.populate_dbs populate_sqlite
     ```

     This creates a SQLite database `agent_search.db` in the `data` directory. This script can be readily adopted to your own bespoke datasets. For a direct installation of the 1TB data into the database, please use [insert link].

2. **Start Qdrant (vector database) Service with Docker**:
   - Run Qdrant service in a Docker container with this command, which sets up the necessary ports and storage:

     ```shell
     docker run -p 6333:6333 -p 6334:6334 \
         -v $(pwd)/qdrant_storage:/qdrant/storage:z \
         qdrant/qdrant
     ```

     For installation guidance on Qdrant, refer to [their documentation](https://qdrant.tech/documentation/quick-start/).

3. **Run the Server**:
   - Launch the AgentSearch server:

     ```shell
     python -m agent_search.app.server
     ```

### Additional Notes

- Run all commands from the root directory of the AgentSearch project.
- Replace the `query` in the run command with your desired search query.
