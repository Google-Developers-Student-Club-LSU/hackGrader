import unittest
import imports

from tests.tools.stats import benchmark_timing, benchmark_stats

class TestScoring(unittest.TestCase):
    @benchmark_stats
    @benchmark_timing
    def test_querying(self) -> None:
        repo: str = "https://github.com/rexim/aoc-2023"
        question: str = f"look at this repository and give it a percent numeric score based on how good the code is: {repo}"
        
        grader = imports.Model()
        answer = grader.query(question)

        print(answer['content'])
        self.assertEqual(answer["status"], 200, "Query failure")

if __name__ == "__main__":
    unittest.main()
