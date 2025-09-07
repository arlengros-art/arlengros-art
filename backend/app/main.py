from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import redis
from rq import Queue
from rq.job import Job

from .tasks import process_prompt

app = FastAPI()

# Redis connection and RQ queue
redis_conn = redis.Redis(host="localhost", port=6379, db=0)
queue = Queue("default", connection=redis_conn)

# Serve frontend static files
frontend_path = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")


class PromptRequest(BaseModel):
    prompt: str


@app.post("/generate")
def generate(req: PromptRequest):
    """Enqueue a job and return its ID."""
    job = queue.enqueue(process_prompt, req.prompt)
    return {"job_id": job.get_id()}


@app.get("/status/{job_id}")
def job_status(job_id: str):
    """Return job status and result if finished."""
    try:
        job = Job.fetch(job_id, connection=redis_conn)
    except Exception:
        return {"status": "not_found", "result": None}
    return {"status": job.get_status(), "result": job.result}
