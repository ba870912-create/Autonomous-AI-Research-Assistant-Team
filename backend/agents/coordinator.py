from crewai import Agent, LLM

def create_citation_manager() -> Agent:
    llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.1)
    return Agent(
        role="Citation Manager",
        goal="Format all references in the requested citation style. "
             "Ensure every claim has a corresponding citation.",
        backstory="You are a meticulous academic editor with deep "
                  "knowledge of citation standards.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3  
    )
from crewai import Agent, LLM

def create_content_analyzer() -> Agent:
    llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.1)
    return Agent(
        role="Content Analyzer",
        goal="Extract key insights, methodologies, findings, "
             "and limitations from each source.",
        backstory="You are an analytical researcher who can "
                  "rapidly distill dense academic text into "
                  "structured, actionable summaries.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )
from crewai import Agent, LLM

def create_coordinator() -> Agent:
    llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.1)
    return Agent(
        role="Research Coordinator",
        goal="Plan and delegate a comprehensive research strategy "
             "by breaking the query into searchable keywords, "
             "selecting relevant sources, and sequencing tasks.",
        backstory="You are a senior research strategist with expertise "
                  "in academic literature and online information sources.",
        llm=llm,
        verbose=True,
        allow_delegation=False,  
        max_iter=3,              
        max_retry_limit=2        
    )
from crewai import Agent, LLM

def create_synthesis_agent() -> Agent:
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",  
        temperature=0.1
    )
    return Agent(
        role="Synthesis Agent",
        goal="Combine analyzed findings into a coherent, "
             "well-structured research report.",
        backstory="You are a scientific writer who transforms "
                  "fragmented research notes into polished reports.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3  
    )
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
