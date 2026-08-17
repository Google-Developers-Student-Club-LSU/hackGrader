import sys

from crawler import Crawler
from driver import Driver
from model import Model

def main() -> None:
    url: str = str(" ".join(sys.argv[1:]))
    if not url:
        raise Exception("Please pass in a URL as an argument")

    driver: Driver = Driver()
    crawler: Crawler = Crawler(url)
    projects: list = crawler.get_projects(driver)
    github_projects: list = crawler.get_github_projects(projects, driver)

    for project in github_projects:
        individual_query(project)

def individual_query(url: str) -> None:
    question: str = f"look at this repository and give it a percent numeric score and explanation for such based on how good the code is: {url}"
    grader = Model()
    answer = grader.query(question)

if __name__ == "__main__":
    main()