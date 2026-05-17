from crewai import Agent
from langchain_anthropic import ChatAnthropic

def create_synthesis_agent() -> Agent:
    # Uses Claude Sonnet for long-form writing
    claude_llm = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        max_tokens=8000
    )
    return Agent(
        role="Synthesis Agent",
        goal="Combine analyzed findings into a coherent,"
             " well-structured research report with clear"
             " sections: introduction, background, main findings,"
             " comparisons, and conclusions.",
        backstory="You are a scientific writer who transforms"
                  " fragmented research notes into polished,"
                  " publication-quality reports.",
        llm=claude_llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )