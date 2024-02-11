from datetime import date, datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from tasks.models import Sprint, Task


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
