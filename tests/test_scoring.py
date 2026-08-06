import unittest
import imports

from tests.tools.stats import timing 

class TestScoring(unittest.TestCase):
    @timing
    def test_querying(self):
        repo: str = "https://github.com/seblague/fluid-sim"
        question: str = f"look at this repository and give it a percent numeric score based on how good the code is: {repo}"
        
        grader = imports.Model()
        answer = grader.query(question)

        print(answer)
        self.assertEqual(answer["status"], 200, "Query failure")

if __name__ == "__main__":
    unittest.main()
