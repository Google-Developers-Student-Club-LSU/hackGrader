import unittest
import imports

from tests.tools.stats import timing 

class TestCrawling(unittest.TestCase):
    @timing
    def test_crawling(self):
        url: str = "https://2026-wics-hackathon.devpost.com"
        crawl = imports.Crawler(url)

if __name__ == "__main__":
    unittest.main()
