import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from app.celery_app import celery

app = FastAPI(title="FastAPI + Celery Demo")


class AddIn(BaseModel):
    x: int
    y: int


class SleepIn(BaseModel):
    seconds: int

    @field_validator("seconds")
    @classmethod
    def non_negative(cls, v):
        if v < 0:
            raise ValueError("seconds must be >= 0")
        return v


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tasks/add")
def submit_add(payload: AddIn):
    task = celery.send_task("app.tasks.add", args=[payload.x, payload.y])
    return {"task_id": task.id}


@app.post("/tasks/long")
def submit_long(payload: SleepIn):
    task = celery.send_task("app.tasks.long_task", args=[payload.seconds])
    return {"task_id": task.id}


@app.get("/tasks/{task_id}")
def task_status(task_id: str):
    async_result = celery.AsyncResult(task_id)
    data = {
        "task_id": task_id,
        "state": async_result.state,
        "meta": async_result.info if isinstance(async_result.info, dict) else {"info": async_result.info},
        "ready": async_result.ready(),
        "successful": async_result.successful() if async_result.ready() else None,
    }
    return data


@app.get("/tasks/{task_id}/result")
def task_result(task_id: str):
    async_result = celery.AsyncResult(task_id)
    if not async_result.ready():
        return {"task_id": task_id, "state": async_result.state, "result": None}
    if async_result.failed():
        raise HTTPException(status_code=500, detail=str(async_result.info))
    return {"task_id": task_id, "result": async_result.get()}
