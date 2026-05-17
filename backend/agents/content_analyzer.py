from crewai import Agent

def create_content_analyzer(llm) -> Agent:
    return Agent(
        role="Content Analyzer",
        goal="Extract key insights, methodologies, findings,"
             " and limitations from each source. Identify"
             " recurring themes across sources.",
        backstory="You are an analytical researcher who can"
                  " rapidly distill dense academic text into"
                  " structured, actionable summaries while"
                  " preserving scientific accuracy.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=5
    )