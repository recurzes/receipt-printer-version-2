import pytest
import json
import hmac
import hashlib
from unittest.mock import patch


def test_webhook_receives_task_added(client):
    payload = {
        "event_name": "item:added",
        "user_id": 12345678,
        "event_data": {
            "id": "7654321",
            "content": "Buy groceries",
            "project_id": "2203306141",
            "priority": 1
        },
        "version": "9"
    }

    with patch('routers.webhooks.handle_task_added') as mock_handler:
        response = client.post("/webhooks/todoist", json=payload)

        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["event"] == "item:added"
        mock_handler.assert_called_once()


def test_webhook_receives_task_completed(client):
    payload = {
        "event_name": "item:completed",
        "user_id": 12345678,
        "event_data": {
            "id": "7654321",
            "content": "Buy groceries"
        },
        "version": "9"
    }

    with patch('routers.webhooks.handle_task_completed') as mock_handler:
        response = client.post("/webhooks/todoist", json=payload)

        assert response.status_code == 200
        mock_handler.assert_called_once()


def test_webhook_signature_verification(client):
    payload = {
        "event_name": "item:added",
        "user_id": 12345678,
        "event_data": {"id": "123", "content": "Test"},
        "version": "9"
    }

    payload_bytes = json.dumps(payload).encode('utf-8')
    client_secret = "test_secret"

    signature = hmac.new(
        client_secret.encode('utf-8'),
        payload_bytes,
        hashlib.sha256
    ).hexdigest()

    with patch('util.config.TODOIST_SECRET', client_secret):
        response = client.post(
            "/webhooks/todoist",
            json=payload,
            headers={"X-Todoist-Hmac-SHA256": signature}
        )

        assert response.status_code == 200


def test_webhook_invalid_signature(client):
    payload = {
        "event_name": "item:added",
        "user_id": 12345678,
        "event_data": {"id": "123", "content": "Test"},
        "version": "9"
    }

    with patch('util.config.TODOIST_SECRET', 'test_secret'):
        response = client.post(
            "/webhooks/todoist",
            json=payload,
            headers={"X-Todoist-Hmac-SHA256": "invalid_signature"}
        )

        assert response.status_code == 401


def test_webhook_invalid_json(client):
    response = client.post(
        "/webhooks/todoist",
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 422
