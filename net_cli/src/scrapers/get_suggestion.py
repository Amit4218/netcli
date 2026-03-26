from bs4 import BeautifulSoup
import requests
from src.utils.constants import SOAP_BASE_URL


def get_movie_recomendations():
    try:
        r = requests.get(f"{SOAP_BASE_URL}/home")
        soup = BeautifulSoup(r.text, "html.parser")

        card_body = soup.select(".col")

        results = []

        for col in card_body:
            results.append({"name": col.text, "link": col.find("a")["href"]})

        return results
    except Exception:
        raise Exception("Error getting movie suggestions")
