import httpx
import os
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

class SerperInput(BaseModel):
    query: str = Field(description="Search query string")
    num_results: int = Field(default=10, description="Number of results")

class SerperSearchTool(BaseTool):
    name: str = "web_search"
    description: str = "Search the web for academic and tech content"
    args_schema: type[BaseModel] = SerperInput

    def _run(self, query: str, num_results: int = 10) -> str:
        url = "https://google.serper.dev/search"
        headers = {
            "X-API-KEY": os.getenv("SERPER_API_KEY"),
            "Content-Type": "application/json"
        }
        payload = {"q": query, "num": num_results}

        with httpx.Client() as client:
            response = client.post(url, json=payload, headers=headers)
            data = response.json()

        results = []
        for item in data.get("organic", []):
            results.append({
                "title": item.get("title"),
                "url": item.get("link"),
                "snippet": item.get("snippet")
            })
        return str(results)
