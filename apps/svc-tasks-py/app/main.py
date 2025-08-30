from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from uuid import UUID

# 👇 add this line so Task and TaskCreate are in scope
from .models import Task, TaskCreate
from .db import insert_task, list_tasks  # if you already created db.py


app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(payload: TaskCreate):
    # simple domain guard: cannot create Done without assignee
    if payload.status == "Done" and not payload.assignee:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Done requires assignee")
    tid = insert_task(payload)
    return Task(id=tid, **payload.model_dump())

@app.get("/tasks")
def get_tasks(projectId: Optional[UUID] = Query(default=None)):
    return list_tasks(projectId)