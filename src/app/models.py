from pydantic import BaseModel
from typing import Optional, List


class TaskCreate(BaseModel):
    content: Optional[str] = None
    description: Optional[str] = None
    project_id: Optional[str] = None
    labels: Optional[List[str]] = None
    priority: Optional[int] = 1
    due_string: Optional[str] = None

class TaskUpdate(BaseModel):
    content: Optional[str] = None
    description: Optional[str] = None
    labels: Optional[List[str]] = None
    priority: Optional[str] = None
    due_string: Optional[str] = None

class WebhookPayload(BaseModel):
    event_name: str
    user_id: int
    event_data: dict
    version: str
    initiator: Optional[dict] = None
