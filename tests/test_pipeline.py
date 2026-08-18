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
        question: str = f"Please provide a concise code review for the following url that includes two percentage scores: The estimated percentage of AI involvement in generating the code. A code goodness score based on the following criteria: cleanliness, readability, functionality, maintainability, scalability, and documentation.Summarize your evaluation clearly and succinctly, highlighting the strengths and areas for improvement in the code. {url}"
        grader = imports.Model()
        answer = grader.query(question)

        print(answer['content'])
        self.assertEqual(answer["status"], 200, "Query failure")

if __name__ == "__main__":
    unittest.main()
