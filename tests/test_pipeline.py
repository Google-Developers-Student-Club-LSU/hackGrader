import unittest
import imports

from tests.tools.stats import benchmark_stats, benchmark_timing

class TestPipeline(unittest.TestCase):
    @benchmark_stats
    def test_pipeline(self) -> None:
        pass

    @benchmark_timing
    def individual_query(self, url: str) -> None:
        pass

if __name__ == "__main__":
    unittest.main()
