from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading
import uuid
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

# In-memory job store
jobs: dict = {}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/research")
async def start_research(req: ResearchRequest):
    job_id = str(uuid.uuid4())
    
    # ✅ Save job immediately before doing anything
    jobs[job_id] = {"status": "running", "result": None}

    # ✅ Run crew in background thread (not blocking)
    def run_job():
        try:
            from backend.crew import run_research_crew
            result = run_research_crew(req.query, req.citation_style)
            jobs[job_id] = {"status": "done", "result": result}
        except Exception as e:
            jobs[job_id] = {"status": "error", "result": str(e)}

    thread = threading.Thread(target=run_job, daemon=True)
    thread.start()

    # ✅ Return job_id immediately (no waiting!)
    return {"job_id": job_id}

@app.get("/research/{job_id}")
async def get_result(job_id: str):
    if job_id not in jobs:
        return {"status": "error", "result": "Job not found"}
    return jobs[job_id]