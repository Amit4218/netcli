from typing import Dict, List

import requests
from src.utils.constants import SOAP_BASE_URL


def search_query(query: str):
    """gets the results based on the query"""

    try:

        params = {"q": query, "limit": 30, "offset": 0}

        r = requests.get(
            f"{SOAP_BASE_URL}/searching",
            params=params,
            headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
        )

        data = r.json()

        results: List[Dict[str, str]] = []

        for movie in data["data"]:
            results.append(
                {
                    "title": movie["t"],
                    "link": f"{SOAP_BASE_URL}/film/{movie['s']}",
                }
            )

        return results
    except Exception:
        raise Exception("Error finding a movie")
