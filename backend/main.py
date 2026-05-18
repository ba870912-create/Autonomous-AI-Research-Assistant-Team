from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import threading
import uuid
import os
import sys
from fastapi.responses import FileResponse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.db.postgres_client import save_job, update_job, get_all_jobs, get_job

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

# In-memory job store (for real-time status)
jobs: dict = {}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/research")
async def start_research(req: ResearchRequest):
    job_id = str(uuid.uuid4())
    
    jobs[job_id] = {"status": "running", "result": None}
    
    # ✅ Save to database
    save_job(job_id=job_id, query=req.query, citation_style=req.citation_style)

    def run_job():
        try:
            from backend.crew import run_research_crew
            result = run_research_crew(req.query, req.citation_style)
            jobs[job_id] = {"status": "done", "result": result}
            # ✅ Update database
            update_job(job_id=job_id, status="done", result=result)
        except Exception as e:
            jobs[job_id] = {"status": "error", "result": str(e)}
            update_job(job_id=job_id, status="error", result=str(e))

    thread = threading.Thread(target=run_job, daemon=True)
    thread.start()
    return {"job_id": job_id}

@app.get("/research/{job_id}")
async def get_result(job_id: str):
    # Check memory first, then database
    if job_id in jobs:
        return jobs[job_id]
    db_job = get_job(job_id)
    if db_job:
        return {"status": db_job["status"], "result": db_job["result"]}
    return {"status": "error", "result": "Job not found"}

# ✅ Research history
@app.get("/history")
async def research_history():
    return {"history": get_all_jobs()}

@app.get("/history/{job_id}")
async def get_history_item(job_id: str):
    job = get_job(job_id)
    if not job:
        return {"status": "error", "result": "Not found"}
    return job

# ✅ ChromaDB endpoints
@app.get("/search-sources")
async def search_sources_endpoint(query: str, n: int = 5):
    from backend.db.chroma_client import search_sources
    results = search_sources(query=query, n_results=n)
    if not results:
        return {"results": []}
    sources = []
    for i, doc in enumerate(results["documents"][0]):
        sources.append({
            "content": doc,
            "url": results["metadatas"][0][i].get("url", ""),
        })
    return {"results": sources}

@app.get("/all-sources")
async def all_sources_endpoint():
    from backend.db.chroma_client import get_all_sources
    results = get_all_sources()
    return {"count": len(results["ids"]) if results else 0}

@app.post("/export-pdf")
async def export_pdf(req: dict):
    """Convert markdown report to PDF and return it"""
    from backend.tools.pdf_export import markdown_to_pdf
    
    markdown_text = req.get("markdown", "")
    job_id = req.get("job_id", "report")
    
    if not markdown_text:
        # Try to get from database
        db_job = get_job(job_id)
        if db_job and db_job.get("result"):
            markdown_text = db_job["result"]
        else:
            return {"error": "No content to export"}
    
    output_path = f"report_{job_id[:8]}.pdf"
    result = markdown_to_pdf(markdown_text, output_path)
    
    if "error" in result.lower():
        return {"error": result}
    
    return FileResponse(
        path=output_path,
        media_type="application/pdf",
        filename="research_report.pdf"
    )