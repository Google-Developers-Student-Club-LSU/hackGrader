import unittest
import imports

from tests.tools.stats import benchmark_timing, benchmark_stats

class TestCrawling(unittest.TestCase):
    @benchmark_stats
    @benchmark_timing
    def test_crawling(self) -> None:
        url: str = "https://2026-wics-hackathon.devpost.com"
        crawl = imports.Crawler(url)

if __name__ == "__main__":
    unittest.main()
