import unittest
from src.fetcher import Fetcher, FetcherError

class TestFetcher(unittest.TestCase):

    def test_fetch_text_from_valid_url(self):
        url = "https://arxiv.org/html/2403.08299v1#S2"
        text = Fetcher.fetch_text_from_url(url)
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)

    def test_fetch_text_from_invalid_url(self):
        url = "https://invalidurl"
        with self.assertRaises(FetcherError):
            Fetcher.fetch_text_from_url(url)

if __name__ == '__main__':
    unittest.main()