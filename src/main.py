from fastapi import FastAPI, HTTPException
from todoist_api_python.api import TodoistAPI
import os

from app.models import TaskCreate, TaskUpdate
from src.util.config import *

app = FastAPI(title="Todoist CRUD API")
todoist = TodoistAPI(TODOIST_API_TOKEN)

@app.post('/tasks/')
async def create_task(task: TaskCreate):
    try:
        new_task = todoist.add_task(
            content=task.content,
            description=task.description,
            project_id=task.project_id,
            labels=task.labels,
            priority=task.priority,
            due_string=task.due_string
        )

        return {
            "id": new_task.id,
            "content": new_task.content,
            "description": new_task.description,
            "project_id": new_task.project_id,
            "labels": new_task.labels,
            "priority": new_task.priority,
            "due": new_task.due.to_dict() if new_task.due else None,
            "is_completed": new_task.is_completed
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    try:
        task = todoist.get_task(task_id=task_id)
        return {
            "id": task.id,
            "content": task.content,
            "description": task.description,
            "project_id": task.project_id,
            "labels": task.labels,
            "priority": task.priority,
            "due": task.due.to_dict() if task.due else None,
            "is_completed": task.is_completed
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Task not found: {str(e)}")

@app.put("/tasks/{task_id}")
async def update_task(task_id: str, task_update: TaskUpdate):
    try:
        updated_task = todoist.update_task(
            task_id=task_id,
            content=task_update.content,
            description=task_update.description,
            labels=task_update.labels,
            priority=task_update.priority,
            due_string=task_update.due_string
        )

        return {
            "id": updated_task.id,
            "content": updated_task.content,
            "description": updated_task.description,
            "labels": updated_task.labels,
            "priority": updated_task.priority,
            "is_completed": updated_task.is_completed
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Failed to update task: {str(e)}")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    try:
        success = todoist.delete_task(task_id=task_id)
        if success:
            return {"message": f"Task {task_id} deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Task not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tasks/{task_id}/complete")
async def complete_task(task_id: str):
    try:
        success = todoist.complete_task(task_id=task_id)
        if success:
            return {"message": f"Task {task_id} marked as completed"}
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {
        "message": "Todoist CRUD API",
        "endpoints": {
            "POST /tasks/": "Create a new task",
            "GET /tasks/": "Get all task",
            "GET /tasks/{task_id}": "Get a specific task",
            "PUT /tasks/{task_id}": "Update a task",
            "DELETE /tasks/{task_id}": "Delete a task",
            "POST /tasks/{task_id}/complete": "Complete a task"
        }
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)