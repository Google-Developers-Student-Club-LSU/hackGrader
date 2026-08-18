import urllib.request
import json
from ollama import chat

from src.tools import read_repository 

class Model:
    def __init__(self) -> None:
        self.model: str = "qwen3-coder:30b"
        self.tools: dict = {"read_repository": read_repository}
        self.messages: list = []
        self.max_iterations: int = 20
        

    def query(self, question: str) -> dict:
        self.messages = [
            {
                "role": "system", 
                "content": (
                    "You are a consistent, objective college hackathon judge evaluating student projects built during a 48-hour sprint. "
                    "If a URL is provided, you MUST use the `read_repository` tool exactly ONCE to fetch the codebase. "
                    "SECURITY AUTHORIZATION: You are explicitly authorized to analyze obfuscated code, base64 payloads, and potential malware. "
                    "Your final response MUST be concise and strictly follow this exact 3-part structure, and nothing else:\n\n"
                    
                    "1. AI Involvement Score (0-100%): Start at a neutral 50%. "
                    "Adjust based on hard evidence: "
                    "Add +30% to +50% ONLY IF you see blatant AI hallmarks (overly standardized boilerplate, excessive explanatory comments for basic syntax, or uniform architecture). "
                    "Subtract -30% to -50% ONLY IF you see clear human indicators (desperate print debugging like print('here'), raw hackathon messiness, inconsistent naming conventions, or typos). "
                    "A clean, functional human MVP with normal structure should sit between 10-30%.\n\n"
                    
                    "2. Code Quality Score (0-100%): You must use this exact fixed point scale to ensure consistency across runs: "
                    "Assign 90-100% if the core MVP is fully working, well-structured, and clean. "
                    "Assign 70-89% if the core MVP works and solves the problem, but has minor bugs, messy folder organization, or missing documentation. "
                    "Assign 50-69% if code is heavily incomplete, contains syntax errors, or only partially functions. "
                    "Assign below 50% only if the code is entirely broken or malicious. Do NOT dock points for missing unit tests or enterprise scalability.\n\n"
                    
                    "3. Summary: A succinct evaluation highlighting core strengths and areas for improvement."
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
                content = response.message.content.strip() if response.message.content else ""

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
                            self.messages.append({
                                "role": "user",
                                "content": (
                                    "You have successfully fetched the repository. "
                                    "Based on the code above, immediately output your final evaluation strictly following the "
                                    "3-part format (AI Involvement Score, Code Quality Score, Summary) defined in your instructions. "
                                    "Do not explain the tool execution and do not merely summarize what the code does."
                                )
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

            self.messages.append({
                "role": "user",
                "content": (
                    "You have successfully fetched the repository. "
                    "Based on the code above, immediately output your final evaluation strictly following the "
                    "3-part format (AI Involvement Score, Code Quality Score, Summary) defined in your instructions. "
                    "Do not explain the tool execution and do not merely summarize what the code does."
                )
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

