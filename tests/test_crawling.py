import unittest
import imports

from tests.tools.stats import timing 

class TestCrawling(unittest.TestCase):
    @timing
    def test_crawling(self):
        pass

if __name__ == "__main__":
    unittest.main()
