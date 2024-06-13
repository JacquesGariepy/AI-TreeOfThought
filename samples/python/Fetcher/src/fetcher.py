import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)

class FetcherError(Exception):
    pass

class Fetcher:
    @staticmethod
    def fetch_text_from_url(url: str) -> str:
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Failed to fetch the URL: {e}")
            raise FetcherError(f"Failed to fetch the URL: {e}")

        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()

        return content #section.get_text(strip=True)