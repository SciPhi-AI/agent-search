import configparser
from typing import List, Optional

import numpy as np

from local_web_search.core import SERPResult


def select_top_urls(
    ordered_points: List[SERPResult],
    max_urls: int = 10,
    url_contains: Optional[List[str]] = None,
) -> List[str]:
    """A function to return the top unique URLs from the given poitns results."""
    if not url_contains:
        url_contains = []

    top_urls = set([])
    for point in ordered_points:
        url = point.url
        if url in top_urls:
            continue
        url_contains_match = False if url_contains else True
        for url_contain in url_contains:
            if url_contain in url:
                url_contains_match = True
                break
        if not url_contains_match:
            continue
        top_urls.add(point.url)
        if len(top_urls) >= max_urls:
            break

    return list(top_urls)


def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Compute the cosine similarity between two vectors."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)


def load_config() -> configparser.ConfigParser:
    # file_path = os.path.join(os.path.dirname(__file__), "..", "config.ini")
    config = configparser.ConfigParser()
    # config.read(file_path)
    config.read("config.ini")
    return config
