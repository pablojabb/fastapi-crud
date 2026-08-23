from enum import Enum

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI()


class Status(str, Enum):
    pending = "pending"
    completed = "completed"


class TaskCreate(BaseModel):
    title: str
    status: Status = Status.pending


class Task(BaseModel):
    id: int
    title: str
    status: Status


tasks = {}


@app.get("/")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
    }


@app.get("/tasks", response_model=list[Task])
def view_tasks(
        limit: int = Query(10, ge=1)
):
    if not tasks:
        raise HTTPException(
            status_code=404,
            detail="No tasks found",
        )

    task_list = list(tasks.values())[:limit]

    return task_list


@app.get("/tasks/{task_id}", response_model=Task)
def view_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    return tasks[task_id]


@app.post(
    "/tasks",
    response_model=Task,
    status_code=201,
)
def create_task(task: TaskCreate):
    new_id = max(tasks.keys(), default=0) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "status": task.status.value,
    }

    tasks[new_id] = new_task

    return new_task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
        task_id: int,
        task: TaskCreate,
):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    updated_task = {
        "id": task_id,
        "title": task.title,
        "status": task.status.value,
    }

    tasks[task_id] = updated_task

    return updated_task


@app.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int):
    if task_id not in tasks:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    deleted_task = tasks.pop(task_id)

    return deleted_task
