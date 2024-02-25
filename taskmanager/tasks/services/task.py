from datetime import date, datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from tasks.exceptions import TaskAlreadyClaimedException
from tasks.models import Epic, Sprint, Task


def can_add_task_to_sprint(task: Task, sprint_id: int) -> bool:
    """
    Check if the task is within the sprint range.
    """
    sprint = get_object_or_404(id=sprint_id)
    return sprint.start_date <= task.created_at.date() <= sprint.end_date


def get_tasks_by_date(by_date: date) -> list:
    """
    Get tasks by date.
    """
    return Task.objects.filter(created_at__date=by_date)


def get_tasks_by_epic(epic_id: int) -> list:
    """
    Get tasks by epic.
    """
    return Task.objects.filter(epic_id=epic_id)


def save_tasks_for_epic(epic_id: int, tasks: list[Task]) -> None:
    """
    Save tasks for an epic.
    """
    epic = get_object_or_404(Epic, id=epic_id)
    epic.tasks.add(*tasks)


def create_task_and_add_to_sprint(
    task_data: dict[str, str],
    sprint_id: int,
    creator: User,
):
    """
    Create a task and add it to the sprint.
    """

    sprint = get_object_or_404(Sprint, id=sprint_id)

    now = datetime.now()

    if not (sprint.start_date <= now <= sprint.end_date):
        raise ValidationError("Cannot add task to sprint. Sprint is not active.")

    with transaction.atomic():
        task = Task.objects.create(
            title=task_data["title"],
            description=task_data.get("description", ""),
            status=task_data.get("status", "UNASSIGNED"),
            creator=creator,
        )

        sprint.tasks.add(task)

    return task


@transaction.atomic
def claim_task(user_id: int, task_id: int) -> None:
    """
    Claim a task.
    """

    # Locks the row for update
    task = Task.objects.select_for_update().get(id=task_id)

    # Check if the task is already claimed
    if task.owner_id:
        raise TaskAlreadyClaimedException("Task already claimed or completed.")

    # Claim the task
    task.owner_id = user_id
    task.status = "IN_PROGRESS"
    task.save()


def claim_task_optimistically(user_id: int, task_id: int) -> None:
    """
    Claim a task optimistically.
    """
    try:
        task = Task.objects.get(id=task_id)
        original_version = task.version

        if task.owner_id:
            raise TaskAlreadyClaimedException("Task already claimed or completed.")

        task.status = "IN_PROGRESS"
        task.owner_id = user_id

        updated_rows = Task.objects.filter(id=task_id, version=original_version).update(
            status="IN_PROGRESS",
            owner_id=user_id,
            version=original_version + 1,
        )

        if updated_rows == 0:
            raise ValidationError("Another transaction updated the task. Please try again.")
    except Task.DoesNotExist:
        raise ValidationError("Task does not exist.")
