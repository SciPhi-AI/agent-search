# LocalSearch [ΨΦ]: A Comprehensive Open Source Framework and Dataset for Webscale Search

LocalSearch is a powerful tool that enables you to operate your very own webscale search engine on a local scale. This repository, along with our open-source initiative, provides access to over one billion high-quality embeddings. These are derived from an extensive collection of content from renowned sources such as Arxiv, Wikipedia, Project Gutenberg, and includes selectively filtered CC data.

We also offer a fully managed access via an API endpoint.

## Quickstart Guide for LocalSearch

Follow this guide for a streamlined setup and demonstration of the LocalSearch project.

### Prerequisites

Make sure Docker is installed on your system. If not, download and install it from [Docker's official website](https://www.docker.com/).

### Quick Setup

1. Install the LocalSearch client by executing:

   ```shell
   git clone https://github.com/SciPhi-AI/local-search.git && cd local-search
   pip install -e .
   ```

### Running a Query

- To perform a query and witness LocalSearch in action, use:

  ```shell
  python local_search/script/run_query.py query --query="What is Fermat's last theorem?"
  ```

  Note that this command assumes you have followed the steps below to launch your local search engine. For remote access to our comprehensive database, please register for a free API key at [SciPhi](https://www.sciphi.ai/).

### Local Setup and Initialization

1. **Database Population**:
   - Populate the SQLite database with this command:

     ```shell
     python local_search/script/populate_dbs.py populate_sqlite
     ```

     This creates a SQLite database `open_web_search.db` in the `data` directory. For a direct installation of the 1TB data into the database, please use [insert link].

2. **Start Qdrant (vector database) Service with Docker**:
   - Run Qdrant service in a Docker container with this command, which sets up the necessary ports and storage:

     ```shell
     docker run -p 6333:6333 -p 6334:6334 \
         -v $(pwd)/qdrant_storage:/qdrant/storage:z \
         qdrant/qdrant
     ```

     For installation guidance on Qdrant, refer to [their documentation](https://qdrant.tech/documentation/quick-start/).

3. **Run the Server**:
   - Launch the LocalSearch server:

     ```shell
     python local_search/app/server.py
     ```

### Additional Notes

- Run all commands from the root directory of the LocalSearch project.
- Replace the `query` in the run command with your desired search query.