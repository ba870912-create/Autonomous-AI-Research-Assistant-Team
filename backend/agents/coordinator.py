from crewai import Agent
from langchain_openai import ChatOpenAI

def create_coordinator(llm) -> Agent:
    return Agent(
        role="Research Coordinator",
        goal="Plan and delegate a comprehensive research strategy"
             " by breaking the query into searchable keywords,"
             " selecting relevant sources, and sequencing tasks.",
        backstory="You are a senior research strategist with expertise"
                  " in academic literature and online information sources."
                  " You excel at decomposing complex topics into targeted"
                  " search strategies.",
        llm=llm,
        verbose=True,
        allow_delegation=True,
        max_iter=3
    )