import unittest, sys
import imports

from tests.tools.stats import benchmark_stats, benchmark_timing

class TestPipeline(unittest.TestCase):
    @benchmark_stats
    def test_pipeline(self) -> None:
        url: str = "https://2026-wics-hackathon.devpost.com"
        driver: Driver = imports.driver.Driver()
        crawler: Crawler = imports.Crawler(url)
        projects: list = crawler.get_projects(driver)
        github_projects: list = crawler.get_github_projects(projects, driver)

        for project in github_projects:
            with self.subTest(project_url=project):
                self.individual_query(project)

    @benchmark_timing
    def individual_query(self, url: str) -> None:
        question: str = f"look at this repository and give it a percent numeric score and explanation for such based on how good the code is: {url}"
        grader = imports.Model()
        answer = grader.query(question)

        print(answer['content'])
        self.assertEqual(answer["status"], 200, "Query failure")

if __name__ == "__main__":
    unittest.main()
