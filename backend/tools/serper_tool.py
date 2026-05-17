import httpx
import os
from crewai.tools import BaseTool  
from pydantic import BaseModel, Field

class SerperInput(BaseModel):
    query: str = Field(description="Search query string")
    num_results: int = Field(default=10, description="Number of results")

class SerperSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the web for academic and tech content"
    args_schema: type[BaseModel] = SerperInput

    def _run(self, query: str, num_results: int = 3) -> str:
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            return "Error: SERPER_API_KEY not set in environment"

        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
        payload = {"q": query, "num": num_results}

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
        except httpx.TimeoutException:
            return "Error: Search request timed out"
        except httpx.HTTPStatusError as e:
            return f"Error: HTTP {e.response.status_code} from Serper API"
        except Exception as e:
            return f"Error: {str(e)}"

        results = []
        for item in data.get("organic", []):
            results.append({
                "title": item.get("title"),
                "url": item.get("link"),
                "snippet": item.get("snippet")
            })

        return str(results) if results else "No results found"
