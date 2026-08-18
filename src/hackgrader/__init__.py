import sys, json

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

def individual_query(url: str) -> str | None:
    question: str = f"Please review the hackathon repository at the following URL: {url}. Provide your evaluation including the two percentage scores and the concise summary of strengths and weaknesses as instructed."
    grader = Model()
    answer = grader.query(question)
    parts = url.rstrip('/').split('/')
    if len(parts) < 2:
        return "Invalid repo"
    owner = parts[-2]
    data = {owner: answer}
    with open("scores.json", 'w', encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()