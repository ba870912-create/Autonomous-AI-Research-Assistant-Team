from crewai import Agent

def create_citation_manager(llm) -> Agent:
    return Agent(
        role="Citation Manager",
        goal="Format all references in the requested citation"
             " style (APA, MLA, or Chicago). Ensure every claim"
             " in the report has a corresponding citation.",
        backstory="You are a meticulous academic editor with deep"
                  " knowledge of citation standards. You ensure"
                  " bibliographic accuracy and completeness.",
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=3
    )
