from model import Model

if __name__ == "__main__":
    repo: str = "https://github.com/seblague/fluid-sim"
    question: str = f"look at this repository and give it a percent numeric score based on how good the code is: {repo}"
    grader = Model()
    answer = grader.query(question)
    print(answer)
