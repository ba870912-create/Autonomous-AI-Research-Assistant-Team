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
