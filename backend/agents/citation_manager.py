from crewai import Agent, LLM

def create_citation_manager() -> Agent:
    llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0.0)
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
