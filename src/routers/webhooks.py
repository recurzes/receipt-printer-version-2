from fastapi import APIRouter, HTTPException, Request, Header
from typing import Optional
from util.config import TODOIST_SECRET
from util.security import verify_webhook_signature

router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
    responses={401: {"description": "Unauthorized Boshet ka"}}
)


@router.post("/todoist")
async def todoist_webhook(
        request: Request,
        x_todoist_hmac_sha256: Optional[str] = Header(None),
        x_todoist_delivery_id: Optional[str] = Header(None)
):
    body = await request.body()

    # TODO: Fix this shet
    # if x_todoist_hmac_sha256:
    #     if not verify_webhook_signature(body, x_todoist_hmac_sha256, TODOIST_SECRET):
    #         raise HTTPException(status_code=401, detail="Invalid webhook signature")

    payload = await request.json()
    event_name = payload.get("event_name")
    event_data = payload.get("event_data")
    user_id = payload.get("user_id")

    print(f"Received webhook: {event_name}")
    print(f"Delivery ID: {x_todoist_delivery_id}")
    print(f"User ID: {user_id}")
    print(f"Event data: {event_data}")

    # Handle different event types:
    if event_name == "item:added":
        await handle_task_added(event_data)
    elif event_name == "item:updated":
        await handle_task_updated(event_data)
    elif event_name == "item:completed":
        await handle_task_completed(event_data)
    elif event_name == "item:uncompleted":
        await handle_task_uncompleted(event_data)
    elif event_name == "item:deleted":
        await handle_task_deleted(event_data)
    elif event_name == "note:added":
        await handle_note_added(event_data)
    elif event_name == "note:updated":
        await handle_note_updated(event_data)
    elif event_name == "note:deleted":
        await handle_note_deleted(event_data)

    print("\n\n")
    return {"status": "Success", "event": event_name}


# Functions
async def handle_task_added(event_data: dict):
    task_id = event_data.get("id")
    content = event_data.get("content")
    print(f"New task added: {content} (ID: {task_id})")


async def handle_task_updated(event_data: dict):
    task_id = event_data.get("id")
    content = event_data.get("content")
    print(f"Task updated: {content} (ID: {task_id})")


async def handle_task_completed(event_data: dict):
    task_id = event_data.get("id")
    content = event_data.get("content")
    print(f"Task completed: {content} (ID: {task_id})")


async def handle_task_uncompleted(event_data: dict):
    task_id = event_data.get("id")
    content = event_data.get("content")
    print(f"Task reopened: {content} (ID: {task_id})")


async def handle_task_deleted(event_data: dict):
    task_id = event_data.get("id")
    print(f"Task deleted: ID {task_id}")


async def handle_note_added(event_data: dict):
    note_id = event_data.get("id")
    content = event_data.get("content")
    print(f"Commend added: {content} (ID: {note_id}")


async def handle_note_updated(event_data: dict):
    note_id = event_data.get("id")
    content = event_data.get("content")
    print(f"Comment updated: {content} (ID: {note_id})")


async def handle_note_deleted(event_data: dict):
    note_id = event_data.get("id")
    print(f"Comment deleted: ID {note_id}")
