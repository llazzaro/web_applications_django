import pytest
from django.contrib.auth.models import Permission
from tasks.models import Task


def test_get_tasks(client, user, auth_headers):
    response = client.get("/", user=user, headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_create_task_not_authorized(client, user):
    response = client.post("/", json={"title": "Test Task", "description": "Test Description"}, user=user)
    assert response.status_code == 401


def test_create_task_forbidden(client, user, auth_headers):
    response = client.post(
        "/", json={"title": "Test Task", "description": "Test Description"}, user=user, headers=auth_headers
    )
    assert response.status_code == 403


def test_create_task(client, user, auth_headers):
    permission = Permission.objects.get(codename="add_task")
    user.user_permissions.add(permission.pk)
    response = client.post(
        "/", json={"title": "Test Task", "description": "Test Description"}, user=user, headers=auth_headers
    )
    assert response.status_code == 201
    assert response.json() == {"title": "Test Task", "description": "Test Description", "id": 1}


def test_get_task(client, user, task, auth_headers):
    response = client.get(f"/{task.id}/", user=user, headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"title": "Test Task", "description": "Test Description", "id": task.id}


def test_update_task(client, user, task, auth_headers):
    response = client.put(
        f"/{task.id}/",
        json={"title": "Updated Task", "description": "Updated Description"},
        user=user,
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json() == {"title": "Updated Task", "description": "Updated Description", "id": task.id}


def test_delete_task(client, user, task, auth_headers):
    response = client.delete(f"/{task.id}/", user=user, headers=auth_headers)

    with pytest.raises(Task.DoesNotExist):
        task = Task.objects.get(id=task.id)

    assert response.status_code == 204
    assert response.content == b""


def test_archived_tasks(client, user, archived_task, auth_headers):
    response = client.get(f"/archive/2024/12/31", user=user, headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {
        "items": [{"title": "Test Task", "description": "Test Description", "id": archived_task.id}],
        "count": 1,
    }


def test_archived_tasks_no_archived_tasks(client, user, task, auth_headers):
    response = client.get(f"/archive/2024/12/31", user=user, headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == {"items": [], "count": 0}
