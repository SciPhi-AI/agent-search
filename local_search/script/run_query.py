import fire
import logging

import requests

from local_search.core import SERPClient

logger = logging.getLogger(__name__)


class QueryWrapper:
    """A wrapper class to run queries on the SERPClient"""

    def __init__(self):
        pass

    def query(self, api_base="http://0.0.0.0:8000"):
        """Run a query on the SERPClient"""
        client = SERPClient(api_base)
        logging.basicConfig(level=logging.INFO)

        try:
            results = client.search("What is a lagrangian?")
            for result in results:
                logging.info(
                    f"URL: {result.url}, Score: {result.score}, Title: {result.title}"
                )
                logging.info(f"Text: {result.text}\n")
                logging.info("-" * 80)
        except requests.HTTPError as e:
            logging.info(f"An error occurred: {e}")


if __name__ == "__main__":
    fire.Fire(QueryWrapper)
