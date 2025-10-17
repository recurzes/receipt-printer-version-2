import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from main import app

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def mock_todoist():
    with patch('util.config.todoist') as mock:
        yield mock

@pytest.fixture
def sample_task():
    return {
        "content": "Buy groceries",
        "description": "Milk, eggs, bread",
        "project_id": "2203306141",
        "labels": ["shopping"],
        "priority": 2,
        "due_string": "tomorrow"
    }

@pytest.fixture
def sample_task_response():
    mock_task = Mock()
    mock_task.id = "7654321"
    mock_task.content = "Buy groceries"
    mock_task.description = "Milk, eggs, bread"
    mock_task.project_id = "2203306141"
    mock_task.labels = ["shopping"]
    mock_task.priority = 2
    mock_task.due = None
    mock_task.is_completed = False
    return mock_task
