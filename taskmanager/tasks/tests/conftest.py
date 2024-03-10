import os

import django
import pytest
from tasks.enums import TaskStatus
from tasks.tests.factories import UserFactory

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskmanager.settings")
django.setup()

from ninja.testing import TestClient
from tasks.api.tasks import api_router
from tasks.models import Task


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def client():
    return TestClient(api_router)


@pytest.fixture
def user():
    user = UserFactory()
    user.save()

    return user


@pytest.fixture
def task(user) -> Task:
    task = Task.objects.create(title="Test Task", description="Test Description", creator=user)
    return task


@pytest.fixture
def archived_task(user) -> Task:
    task = Task.objects.create(
        title="Test Task", description="Test Description", creator=user, status=TaskStatus.ARCHIVED.value
    )
    task.created_at = "2022-12-31"
    task.save()
    return task
