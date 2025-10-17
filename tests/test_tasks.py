import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient


def test_create_task_success(client, mock_todoist, sample_task, sample_task_response):
    mock_todoist.add_task.return_value = sample_task_response

    response = client.post("/tasks/", json=sample_task)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "7654321"
    assert data["content"] == "Buy groceries"
    assert data["description"] == "Milk, eggs, bread"
    assert data["labels"] == ["shopping"]
    assert data["priority"] == 2
    assert data["is_completed"] == False

    mock_todoist.add_task.assert_called_once_with(
        content="Buy groceries",
        description="Milk, eggs, bread",
        project_id="2203306141",
        labels=["shopping"],
        priority=2,
        due_string="tomorrow"
    )


def test_create_task_minimal_data(client, mock_todoist):
    mock_task = Mock()
    mock_task.id = "123456"
    mock_task.content = "Simple task"
    mock_task.description = None
    mock_task.project_id = None
    mock_task.labels = []
    mock_task.priority = 1
    mock_task.due = None
    mock_task.is_completed = False

    mock_todoist.add_task.return_value = mock_task

    response = client.post("/tasks/", json={"content": "Simple task"})

    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Simple task"
    assert data["priority"] == 1


def test_create_task_api_error(client, mock_todoist):
    mock_todoist.add_task.side_effect = Exception("API Error")

    response = client.post("/tasks/", json={"content": "Test task"})

    assert response.status_code == 500
    assert "API Error" in response.json()["detail"]


def test_get_all_tasks_success(client, mock_todoist):
    mock_task1 = Mock()
    mock_task1.id = "1"
    mock_task1.content = "Task 1"
    mock_task1.description = "Description 1"
    mock_task1.project_id = "123"
    mock_task1.labels = ["work"]
    mock_task1.priority = 3
    mock_task1.is_completed = False

    mock_task2 = Mock()
    mock_task2.id = "2"
    mock_task2.content = "Task 2"
    mock_task2.description = "Description 2"
    mock_task2.project_id = "456"
    mock_task2.labels = ["personal"]
    mock_task2.priority = 1
    mock_task2.is_completed = False

    mock_todoist.get_tasks.return_value = [mock_task1, mock_task2]

    response = client.get("/tasks/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["content"] == "Task 1"
    assert data[1]["content"] == "Task 2"


def test_get_all_tasks_empty(client, mock_todoist):
    mock_todoist.get_tasks.return_value = []

    response = client.get("/tasks/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_task_by_id_success(client, mock_todoist, sample_task_response):
    mock_todoist.get_task.return_value = sample_task_response

    response = client.get("/tasks/7654321")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "7654321"
    assert data["content"] == "Buy groceries"

    mock_todoist.get_task.assert_called_once_with(task_id="7654321")


def test_get_task_by_id_not_found(client, mock_todoist):
    mock_todoist.get_task.side_effect = Exception("Task not found")

    response = client.get("/tasks/nonexistent")

    assert response.status_code == 404
    assert "Task not found" in response.json()["detail"]


def test_update_task_success(client, mock_todoist):
    mock_updated_task = Mock()
    mock_updated_task.id = "7654321"
    mock_updated_task.content = "Updated task"
    mock_updated_task.description = "Updated description"
    mock_updated_task.labels = ["updated"]
    mock_updated_task.priority = 4
    mock_updated_task.is_completed = False

    mock_todoist.update_task.return_value = mock_updated_task

    update_data = {
        "content": "Updated task",
        "description": "Updated description",
        "priority": 4
    }

    response = client.put("/tasks/7654321", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Updated task"
    assert data["priority"] == 4


def test_update_task_partial(client, mock_todoist):
    mock_updated_task = Mock()
    mock_updated_task.id = "7654321"
    mock_updated_task.content = "Original task"
    mock_updated_task.description = "Updated description only"
    mock_updated_task.labels = []
    mock_updated_task.priority = 1
    mock_updated_task.is_completed = False

    mock_todoist.update_task.return_value = mock_updated_task

    response = client.put("/tasks/7654321", json={"description": "Updated description only"})

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated description only"


def test_update_task_not_found(client, mock_todoist):
    mock_todoist.update_task.side_effect = Exception("Task not found")

    response = client.put("/tasks/nonexistent", json={"content": "Updated"})

    assert response.status_code == 404


def test_delete_task_success(client, mock_todoist):
    mock_todoist.delete_task.return_value = True

    response = client.delete("/tasks/7654321")

    assert response.status_code == 200
    assert response.json()["message"] == "Task 7654321 deleted successfully"

    mock_todoist.delete_task.assert_called_once_with(task_id="7654321")


def test_delete_task_not_found(client, mock_todoist):
    mock_todoist.delete_task.return_value = False

    response = client.delete("/tasks/nonexistent")

    assert response.status_code == 404


def test_delete_task_api_error(client, mock_todoist):
    mock_todoist.delete_task.side_effect = Exception("API Error")

    response = client.delete("/tasks/7654321")

    assert response.status_code == 500


def test_complete_task_success(client, mock_todoist):
    mock_todoist.close_task.return_value = True

    response = client.post("/tasks/7654321/complete")

    assert response.status_code == 200
    assert response.json()["message"] == "Task 7654321 marked as completed"

    mock_todoist.close_task.assert_called_once_with(task_id="7654321")


def test_complete_task_not_found(client, mock_todoist):
    mock_todoist.close_task.return_value = False

    response = client.post("/tasks/nonexistent/complete")

    assert response.status_code == 404


def test_complete_task_api_error(client, mock_todoist):
    mock_todoist.close_task.side_effect = Exception("API Error")

    response = client.post("/tasks/7654321/complete")

    assert response.status_code == 500
