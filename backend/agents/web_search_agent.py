from crewai import Agent, LLM
from backend.tools.serper_tool import SerperSearchTool
from backend.tools.arxiv_tool import ArxivSearchTool
from backend.tools.scraper_tool import WebScraperTool

def create_web_search_agent() -> Agent:
    llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.1)
    return Agent(
        role="Web Search Agent",
        goal="Gather high-quality information from academic "
             "databases, tech blogs, and documentation sites.",
        backstory="You are an expert researcher who knows how to "
                  "find authoritative sources quickly.",
        llm=llm,
        tools=[
            SerperSearchTool(),
            ArxivSearchTool(),
            WebScraperTool()
        ],
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )
