from crewai import Agent, LLM

def create_synthesis_agent() -> Agent:
    llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.1)
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
