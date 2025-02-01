from fastapi import FastAPI, HTTPException, status, Depends, Request
from pydantic import BaseModel, Field, conint
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()

# Get the API key securely from environment variables
API_KEY = os.getenv("LAB4_API_KEY")

app = FastAPI()

# Mock Databases
task_db: List[dict] = [{"task_id": 1, "task_title": "Laboratory Activity", "task_desc": "Create Lab Act 2", "is_finished": False}]
tasks: List[dict] = [{"id": 1, "name": "Task 1", "description": "Description 1"}]

# Models
class TaskV1(BaseModel):
    task_id: conint(gt=0)
    task_title: str = Field(..., min_length=1)
    task_desc: str = Field(default="", max_length=255)
    is_finished: bool = Field(default=False)

class TaskV2(BaseModel):
    name: str = Field(..., example="Task 1")
    description: str = Field(..., example="Description of Task 1")

# API Key Dependency
def check_api_key(api_key: str = None):
    if api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
    return True

# Version 1 Endpoints
@app.post("/v1/tasks")
def add_task_v1(task: TaskV1):
    if any(t['task_id'] == task.task_id for t in task_db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task ID already exists")
    task_db.append(task.dict())
    return {"status": "ok", "task": task.dict()}

@app.get("/v1/tasks/{task_id}")
def get_task_v1(task_id: int):
    task = next((t for t in task_db if t["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"status": "ok", "task": task}

@app.patch("/v1/tasks/{task_id}")
def update_task_v1(task_id: int, updated_task: TaskV1):
    for idx, task in enumerate(task_db):
        if task["task_id"] == task_id:
            task_db[idx].update(updated_task.dict(exclude_unset=True))
            return {"status": "ok", "task": task_db[idx]}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@app.delete("/v1/tasks/{task_id}")
def delete_task_v1(task_id: int):
    task = next((t for t in task_db if t["task_id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task_db.remove(task)
    return {"status": "ok", "task": task}

# Version 2 Endpoints
@app.post("/v2/tasks", status_code=status.HTTP_201_CREATED)
async def add_task_v2(task: TaskV2, api_key: str = Depends(check_api_key)):
    if any(t["name"] == task.name for t in tasks):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Task name already exists")
    new_task = task.dict()
    new_task["id"] = len(tasks) + 1
    tasks.append(new_task)
    return new_task

@app.get("/v2/tasks/{task_id}")
async def get_task_v2(task_id: int, api_key: str = Depends(check_api_key)):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@app.put("/v2/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_task_v2(task_id: int, updated_task: TaskV2, api_key: str = Depends(check_api_key)):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    task.update(updated_task.dict())
    return None

@app.delete("/v2/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_v2(task_id: int, api_key: str = Depends(check_api_key)):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    tasks.remove(task)
    return None
