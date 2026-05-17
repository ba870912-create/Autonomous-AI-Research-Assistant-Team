from crewai import Agent
from backend.tools.serper_tool import SerperSearchTool
from backend.tools.arxiv_tool import ArxivSearchTool
from backend.tools.scraper_tool import WebScraperTool

def create_web_search_agent(llm) -> Agent:
    return Agent(
        role="Web Search Agent",
        goal="Gather high-quality information from academic"
             " databases, tech blogs, and documentation sites.",
        backstory="You are an expert researcher who knows how to"
                  " find authoritative sources quickly. You prioritize"
                  " peer-reviewed papers and reputable technical blogs.",
        llm=llm,
        tools=[
            SerperSearchTool(),
            ArxivSearchTool(),
            WebScraperTool()
        ],
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )