import arxiv
from crewai_tools import BaseTool
from pydantic import BaseModel, Field

class ArxivInput(BaseModel):
    query: str = Field(description="Research topic to search on arXiv")
    max_results: int = Field(default=5)

class ArxivSearchTool(BaseTool):
    name: str = "arxiv_search"
    description: str = "Search arXiv for academic papers"
    args_schema: type[BaseModel] = ArxivInput

    def _run(self, query: str, max_results: int = 5) -> str:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )
        papers = []
        for paper in client.results(search):
            papers.append({
                "title": paper.title,
                "authors": [a.name for a in paper.authors],
                "abstract": paper.summary[:500],
                "url": paper.entry_id,
                "published": str(paper.published.date()),
                "pdf_url": paper.pdf_url
            })
        return str(papers)
