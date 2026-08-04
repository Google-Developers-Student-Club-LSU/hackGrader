import urllib.request
import json

def read_repository(url: str) -> str:
    """
    Recursively fetches all the source code files from a GitHub repository URL.
    """

    max_chars: int = 40000
    current_chars: int = 0
    output: str = ""

    parts = url.rstrip('/').split('/')
    if len(parts) < 2:
        return "Invalid repo"
    owner, repo = parts[-2], parts[-1]

    try:
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        request = urllib.request.Request(api_url, headers={"User-Agent": "Ollama-Local-Agent"})
        with urllib.request.urlopen(request) as response:
            repo_data = json.loads(response.read().decode())
            branch = repo_data.get("default_branch", "main")

        tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
        request = urllib.request.Request(tree_url, headers={"User-Agent": "Ollama-Local-Agent"})
        with urllib.request.urlopen(request) as response:
            tree_data = json.loads(response.read().decode())

        files = [item for item in tree_data.get("tree", []) if item.get("type") == "blob"]
        for file in files:
            file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file['path']}"
            request = urllib.request.Request(file_url, headers={"User-Agent": "Ollama-Local-Agent"})
            try:
                with urllib.request.urlopen(request) as response:
                    content = response.read().decode("utf-8", errors="ignore")

                    if current_chars + len(content) > max_chars:
                        break

                    output += content
                    current_chars += len(content)
            except Exception as e:
                output += f"Error reading: {e}"

        return output

    except Exception as e:
        return f"Error: {e}"
