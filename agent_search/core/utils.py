import configparser
import os
from typing import List, Optional

import numpy as np

from agent_search.core import SERPResult


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


def get_data_path() -> str:
    return os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "data",
    )


def load_config(config_dir: Optional[str] = None) -> configparser.ConfigParser:
    """Load the configuration file."""
    config = configparser.ConfigParser()
    if not config_dir:
        config_dir = get_data_path()
    config.read(os.path.join(config_dir, "config.ini"))
    return config
