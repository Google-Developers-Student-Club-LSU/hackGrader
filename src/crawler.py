from src import driver

class Crawler:
    def __init__(self, link: str) -> None:
        self.base_url: str = link
        self.project_url: str = self.base_url + '/project-gallery'
        self.queue: list = list()

        web_driver = driver.Driver()


