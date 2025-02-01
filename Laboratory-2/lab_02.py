from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()


task_db = [
    {"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}
]


class Task(BaseModel):
    task_title: str = Field(..., min_length=1)
    task_desc: Optional[str] = None
    is_finished: bool = False


def get_task(task_id: int):
    return next((task for task in task_db if task['task_id'] == task_id), None)


@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "ok", "task": task}


@app.post("/tasks")
async def create_task(task: Task):
    new_id = len(task_db) + 1
    task_data = {"task_id": new_id, **task.dict()}
    task_db.append(task_data)
    return {"status": "ok", "task": task_data}

@app.patch("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    task_data = get_task(task_id)
    if task_data is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_data["task_title"] = task.task_title
    task_data["task_desc"] = task.task_desc
    task_data["is_finished"] = task.is_finished
    return {"status": "ok", "task": task_data}

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task_db.remove(task)
    return {"status": "ok"}
