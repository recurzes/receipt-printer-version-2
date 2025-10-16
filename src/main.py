from fastapi import FastAPI

import routers.webhooks
import routers.tasks
from src.util.config import *

app = FastAPI(title="Todoist CRUD API")
todoist = TodoistAPI(TODOIST_API_TOKEN)

app.include_router(routers.webhooks.router)
app.include_router(routers.tasks.router)

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
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)