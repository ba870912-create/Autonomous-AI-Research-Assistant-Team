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
