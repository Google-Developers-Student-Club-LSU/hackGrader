import unittest
import imports

from tests.tools.stats import benchmark_timing, benchmark_stats

class TestCrawling(unittest.TestCase):
    @benchmark_stats
    @benchmark_timing
    def test_crawling(self) -> None:
        url: str = "https://2026-wics-hackathon.devpost.com"
        driver = imports.driver.Driver()
        crawl = imports.Crawler(url)

        urls = crawl.get_projects(driver)
        github = crawl.get_github_projects(urls, driver)

        self.assertEqual(len(github) > 0, True, "Query failure")

if __name__ == "__main__":
    unittest.main()
