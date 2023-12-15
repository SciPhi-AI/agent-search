import logging

import fire
import requests

from agent_search.core import SERPClient

logger = logging.getLogger(__name__)


class QueryDemo:
    """A wrapper class to run queries on the SERPClient"""

    def __init__(self):
        pass

    def run(
        self,
        query="What is a lagrangian?",
        api_base="https://api.sciphi.ai",
    ):
        """Run a search with the SERPClient"""
        client = SERPClient(api_base)
        logging.basicConfig(level=logging.INFO)

        try:
            results = client.search(query)
            for i, result in enumerate(results):
                logging.info(
                    f"{i+1}. \033[94mURL: {result.url}\033[0m (Score: \033[95m{result.score:.2f}\033[0m)"
                )
                logging.info("-" * 50)
                logging.info(f"Title: \033[93m{result.title}\033[0m")
                logging.info(f"Text:\n{result.text}\n")
                # logging.info(f"Metadata:\n{result.metadata}...")
                logging.info("-" * 80)

        except requests.HTTPError as e:
            logging.info(f"An error occurred: {e}")


if __name__ == "__main__":
    fire.Fire(QueryDemo)
