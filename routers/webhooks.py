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