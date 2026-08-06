import unittest
import imports

from tests.tools.stats import timing 

class TestPipeline(unittest.TestCase):
    @timing
    def test_pipeline(self):
        pass

if __name__ == "__main__":
    unittest.main()
