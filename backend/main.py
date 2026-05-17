from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio, uuid
#from backend.crew import run_research_crew

app = FastAPI(title="AI Research Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ResearchRequest(BaseModel):
    query: str
    citation_style: str = "APA"

# Simple in-memory job store (use Redis/DB in production)
jobs: dict = {}

@app.post("/research")
async def start_research(req: ResearchRequest, bg: BackgroundTasks):
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "running", "result": None}

    def run_job():
        try:
            result = run_research_crew(req.query, req.citation_style)
            jobs[job_id] = {"status": "done", "result": result}
        except Exception as e:
            jobs[job_id] = {"status": "error", "result": str(e)}

    bg.add_task(run_job)
    return {"job_id": job_id}

@app.get("/research/{job_id}")
async def get_result(job_id: str):
    if job_id not in jobs:
        return {"error": "Job not found"}
    return jobs[job_id]

@app.get("/health")
async def health():
    return {"status": "ok"}