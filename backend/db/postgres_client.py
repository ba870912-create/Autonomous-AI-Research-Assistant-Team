from sqlalchemy import create_engine, Column, String, Text, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./research_history.db")

# Use SQLite as fallback (no setup needed)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class ResearchHistory(Base):
    __tablename__ = "research_history"

    id = Column(String, primary_key=True)
    query = Column(String, nullable=False)
    citation_style = Column(String, default="APA")
    status = Column(String, default="running")
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

def save_job(job_id: str, query: str, citation_style: str):
    db = SessionLocal()
    try:
        job = ResearchHistory(
            id=job_id,
            query=query,
            citation_style=citation_style,
            status="running"
        )
        db.add(job)
        db.commit()
    except Exception as e:
        print(f"DB save error: {e}")
    finally:
        db.close()

def update_job(job_id: str, status: str, result: str):
    db = SessionLocal()
    try:
        job = db.query(ResearchHistory).filter(ResearchHistory.id == job_id).first()
        if job:
            job.status = status
            job.result = result
            job.updated_at = datetime.utcnow()
            db.commit()
    except Exception as e:
        print(f"DB update error: {e}")
    finally:
        db.close()

def get_all_jobs():
    db = SessionLocal()
    try:
        jobs = db.query(ResearchHistory).order_by(
            ResearchHistory.created_at.desc()
        ).all()
        return [
            {
                "id": j.id,
                "query": j.query,
                "citation_style": j.citation_style,
                "status": j.status,
                "created_at": str(j.created_at),
                "has_result": j.result is not None
            }
            for j in jobs
        ]
    except Exception as e:
        print(f"DB get error: {e}")
        return []
    finally:
        db.close()

def get_job(job_id: str):
    db = SessionLocal()
    try:
        job = db.query(ResearchHistory).filter(ResearchHistory.id == job_id).first()
        if job:
            return {
                "id": job.id,
                "query": job.query,
                "citation_style": job.citation_style,
                "status": job.status,
                "result": job.result,
                "created_at": str(job.created_at)
            }
        return None
    except Exception as e:
        print(f"DB get job error: {e}")
        return None
    finally:
        db.close()