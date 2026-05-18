from crewai import Crew, Task, Process
from dotenv import load_dotenv
from backend.agents.coordinator import create_coordinator
from backend.agents.web_search_agent import create_web_search_agent
from backend.agents.content_analyzer import create_content_analyzer
from backend.agents.synthesis_agent import create_synthesis_agent
from backend.agents.citation_manager import create_citation_manager
import time

load_dotenv()

def run_research_crew(query: str, citation_style: str = "APA") -> str:
    coordinator = create_coordinator()
    searcher    = create_web_search_agent()
    analyzer    = create_content_analyzer()
    synthesizer = create_synthesis_agent()
    citer       = create_citation_manager()

    t1 = Task(
        description="Create a search plan for: {query}. "
                    "Output 3-5 search keywords and list source types.",
        expected_output="Structured search plan with keywords and source list",
        agent=coordinator
    )
    t2 = Task(
        description="Execute the search plan. Search the web and arXiv. "
                    "Scrape top 3 URLs only. Return raw content per source.",
        expected_output="List of sources with titles, URLs, and raw text",
        agent=searcher,
        context=[t1]
    )
    t3 = Task(
        description="Analyze each source briefly. Extract: key findings, "
                    "methods, year. Identify 2-3 cross-source themes.",
        expected_output="Brief analysis per source + thematic summary",
        agent=analyzer,
        context=[t2]
    )
    t4 = Task(
        description="Write a research report on: {query}. "
                    "Sections: Abstract, Introduction, Findings, Conclusion. "
                    "Keep it concise — around 800 words.",
        expected_output="Markdown research report",
        agent=synthesizer,
        context=[t3]
    )
    t5 = Task(
        description="Add {citation_style} citations to the report. "
                    "Add References section.",
        expected_output="Final report with citations and references",
        agent=citer,
        context=[t4, t2],
        output_file="report.md"
    )

    crew = Crew(
        agents=[coordinator, searcher, analyzer, synthesizer, citer],
        tasks=[t1, t2, t3, t4, t5],
        process=Process.sequential,
        verbose=True
    )

    # ✅ Retry logic for rate limit errors
    max_retries = 3
    for attempt in range(max_retries):
        try:
            result = crew.kickoff(inputs={"query": query, "citation_style": citation_style})
            return result.raw if result.raw else str(result)
        except Exception as e:
            error_msg = str(e)
            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                wait_time = 30 * (attempt + 1)  # 30s, 60s, 90s
                print(f"Rate limit hit. Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
                time.sleep(wait_time)
            else:
                return f"Research crew failed: {error_msg}"
    
    return "Research failed after 3 retries due to rate limits. Please try again in a few minutes."