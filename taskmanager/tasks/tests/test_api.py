import pytest
from tasks.models import Task


def test_get_tasks(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client, user):
    response = client.post("/", json={"title": "Test Task", "description": "Test Description"}, user=user)
    assert response.status_code == 201
    assert response.json() == {"title": "Test Task", "description": "Test Description", "id": 1}


def test_get_task(client, user, task):
    response = client.get(f"/{task.id}/")
    assert response.status_code == 200
    assert response.json() == {"title": "Test Task", "description": "Test Description", "id": task.id}


def test_update_task(client, user, task):
    response = client.put(
        f"/{task.id}/", json={"title": "Updated Task", "description": "Updated Description"}, user=user
    )
    assert response.status_code == 200
    assert response.json() == {"title": "Updated Task", "description": "Updated Description", "id": task.id}


def test_delete_task(client, user, task):
    response = client.delete(f"/{task.id}/", user=user)

    with pytest.raises(Task.DoesNotExist):
        task = Task.objects.get(id=task.id)

    assert response.status_code == 204
    assert response.content == b""
