import urllib.request
import json
from ollama import chat

from src.tools import read_repository 

class Model:
    def __init__(self) -> None:
        self.model: str = "qwen2.5-coder:7b"
        self.tools: dict = {"read_repository": read_repository}
        self.messages: list = []
        self.max_iterations: int = 20
        

    def query(self, question: str) -> dict:
        self.messages = [
                    {
                        "role": "system", 
                         "content": (
                            "You are an expert senior code reviewer. You must follow this strict two-step process:"
                            "STEP 1: You MUST use the `read_repository` tool exactly ONCE to fetch the codebase."
                            "STEP 2: Once you receive the tool's output, you are STRICTLY FORBIDDEN from calling ANY tools again."
                            "You must immediately output your final response, which must include a numeric percent score (0-100)"
                            "and a detailed explanation of the code quality based on the provided text."
                            "Do not attempt to paginate, re-read, or fetch more data."
                        )
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
        for _ in range(self.max_iterations):
            try:
                response = chat(
                    model = self.model,
                    messages = self.messages,
                    tools = [read_repository],
                    options = {"num_ctx": 16384} # the number is 16k tokens which is medium sized apparently
                )
            except Exception as e:
                return {"status": 500, "content": f"Error during chat: {e}"}

            self.messages.append(response.message)

            if not response.message.tool_calls:
                content = response.message.content.strip()

                if content.startswith("```"):
                    content = content.replace("```json", "").replace("```", "").strip()

                try:
                    parsed_content = json.loads(content)
                    if isinstance(parsed_content, dict) and "name" in parsed_content:
                        func_name = parsed_content["name"]
                        args = parsed_content["arguments"]

                        if func_name in self.tools:
                            result = self.tools[func_name](**args)
                            self.messages.append({
                                "role": "tool",
                                "content": str(result),
                                "tool_name": func_name
                            })
                            continue
                except json.JSONDecodeError:
                    pass
                
                return {"status": 200, "content": response.message.content or "No response"}

            for tool_call in response.message.tool_calls:
                result = self._execute_tool(tool_call)
                self.messages.append({
                    "role": "tool",
                    "content": result,
                    "tool_name": tool_call.function.name
                })

        return {"status": 408, "content": "Max iterations completed"}

    def _execute_tool(self, tool_call) -> str:
        func_name = tool_call.function.name
        args = tool_call.function.arguments

        if func_name not in self.tools:
            return f"{func_name} not found in tools"

        try:
            result = self.tools[func_name](**args)
            return str(result)

        except Exception as e:
            return f"Tool error: {e}"

