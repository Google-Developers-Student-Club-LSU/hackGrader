import asyncio, aiohttp

def read_repository(url: str) -> str:
    """
    Synchronous wrapper that starts the async event loop without breaking model.py.
    Recursively fetches all the source code files from a GitHub repository URL.
    """
    return asyncio.run(_async_read_repository(url))

async def _async_read_repository(url: str) -> str:
    max_chars: int = 40000
    current_chars: int = 0
    output: str = ""

    parts = url.rstrip('/').split('/')
    if len(parts) < 2:
        return "Invalid repo"
    owner, repo = parts[-2], parts[-1]

    if repo.endswith('.git'):
        repo = repo[:-4]

    timeout = aiohttp.ClientTimeout(total=None, sock_connect=60, sock_read=60)
    semaphore = asyncio.Semaphore(10)

    async def fetch_with_retry(session, fetch_url, is_json=False):
        while True:
            try:
                async with semaphore:
                    async with session.get(fetch_url) as response:
                        if response.status in (403, 429):
                            await asyncio.sleep(5)
                            continue
                            
                        response.raise_for_status()
                        if is_json:
                            return await response.json()
                        else:
                            return await response.text(errors="ignore")
                            
            except (aiohttp.ClientError, asyncio.TimeoutError):
                await asyncio.sleep(3)

    try:
        async with aiohttp.ClientSession(headers={"User-Agent": "Ollama-Local-Agent"}, timeout=timeout) as session:
            api_url = f"https://api.github.com/repos/{owner}/{repo}"
            repo_data = await fetch_with_retry(session, api_url, is_json=True)
            branch = repo_data.get("default_branch", "main")

            tree_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"
            tree_data = await fetch_with_retry(session, tree_url, is_json=True)

            files = [item for item in tree_data.get("tree", []) if item.get("type") == "blob"]
            
            tasks = []
            for file in files:
                file_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{file['path']}"
                tasks.append(fetch_with_retry(session, file_url, is_json=False))

            for future in asyncio.as_completed(tasks):
                content = await future
                
                if current_chars + len(content) > max_chars:
                    break
                    
                output += content
                current_chars += len(content)    

        return output

    except Exception as e:
        return f"Error: {e}"
