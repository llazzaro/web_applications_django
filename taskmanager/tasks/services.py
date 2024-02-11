from datetime import date

from django.shortcuts import get_object_or_404
from tasks.models import Task


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
