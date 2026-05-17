from crewai import Crew, Task, Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from backend.agents.coordinator import create_coordinator
from backend.agents.web_search_agent import create_web_search_agent
from backend.agents.content_analyzer import create_content_analyzer
from backend.agents.synthesis_agent import create_synthesis_agent
from backend.agents.citation_manager import create_citation_manager

load_dotenv()

def run_research_crew(query: str, citation_style: str = "APA") -> str:
    gpt4 = ChatOpenAI(model="gpt-4o", temperature=0.1)

    coordinator = create_coordinator(gpt4)
    searcher    = create_web_search_agent(gpt4)
    analyzer    = create_content_analyzer(gpt4)
    synthesizer = create_synthesis_agent()        # uses Claude
    citer       = create_citation_manager(gpt4)

    t1 = Task(
        description=f"Create a search plan for: {query}. "
                    "Output 5-8 search keywords and list source types.",
        expected_output="Structured search plan with keywords and source list",
        agent=coordinator
    )
    t2 = Task(
        description="Execute the search plan. Search the web and arXiv."
                    " Scrape top 5 URLs. Return raw content per source.",
        expected_output="List of sources with titles, URLs, and raw text",
        agent=searcher,
        context=[t1]
    )
    t3 = Task(
        description="Analyze each source. Extract: key findings, methods,"
                    " limitations, year. Identify 3-5 cross-source themes.",
        expected_output="Structured analysis per source + thematic summary",
        agent=analyzer,
        context=[t2]
    )
    t4 = Task(
        description=f"Write a comprehensive research report on: {query}."
                    " Sections: Abstract, Introduction, Background, "
                    "Findings, Discussion, Conclusion. Min 1500 words.",
        expected_output="Full markdown research report",
        agent=synthesizer,
        context=[t3]
    )
    t5 = Task(
        description=f"Add {citation_style} citations to the report."
                    " Every claim needs a citation. Add References section.",
        expected_output="Final report with inline citations and references",
        agent=citer,
        context=[t4, t2]
    )

    crew = Crew(
        agents=[coordinator, searcher, analyzer, synthesizer, citer],
        tasks=[t1, t2, t3, t4, t5],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    return result.raw