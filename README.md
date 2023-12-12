# LocalSearch [ΨΦ]: An open source framework and dataset for webscale search

## Quickstart Guide for LocalSearch

This guide will walk you through the steps to quickly set up and run a demonstration of the LocalSearch project.

### Prerequisites

Ensure you have Docker installed on your machine. If not, you can download and install it from [Docker's official website](https://www.docker.com/).

### Quick Setup

- To install the LocalSearch client, run the following:

```shell
git clone https://github.com/SciPhi-AI/local-search.git && cd local-search
pip install -e .
```

### Running a Query

- To execute a query and see the LocalSearch in action, use the following command:
  
  ```shell
  python local_search/script/run_query.py query --query="What is Fermat's last theorem?"
  ```

  Please register with [SciPhi](https://www.sciphi.ai/) for a free API key for remote access to the entire database.

### Local Setup and Initialization

1. **Database Population**:
   - Run the following command to populate the SQLite database:

     ```shell
     python local_search/script/populate_dbs.py populate_sqlite
     ```

     This will create a SQLite database named `open_web_search.db` in the `data` directory. It would be rather slow to stream the entire 1tb of data into the database, so the database can be installed directly from [insert link].

2. **Start Qdrant (vector database) Service with Docker**:
   - Execute the following command to run the Qdrant service in a Docker container. This step will expose the necessary ports and set up the volume for Qdrant storage:

     ```shell
     docker run -p 6333:6333 -p 6334:6334 \
         -v $(pwd)/qdrant_storage:/qdrant/storage:z \
         qdrant/qdrant
     ```

     For help installing Qdrant, please refer to [their documentation here](https://qdrant.tech/documentation/quick-start/).

3. **Run the Server**:
   - Start the LocalSearch server by executing:

     ```shell
     python local_search/app/server.py
     ```

### Notes

- Ensure all commands are run from the root directory of the LocalSearch project.
- Modify the `query` in the last step with your specific search query.