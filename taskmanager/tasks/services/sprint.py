from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from tasks.models import Epic, Sprint, Task


def create_sprint(sprint_data: dict[str, str], creator: User) -> Sprint:
    """
    Create a sprint.
    """
    sprint = Sprint.objects.create(
        name=sprint_data["name"],
        description=sprint_data.get("description", ""),
        start_date=sprint_data["start_date"],
        end_date=sprint_data["end_date"],
        creator=creator,
    )
    sprint.save()

    return sprint


@transaction.atomic
def remove_task_from_sprint(task_id: int, sprint_id: int) -> None:
    """
    Remove a task from a sprint.
    """
    sprint = Sprint.objects.select_for_updae().get(id=sprint_id)
    task = Task.objects.get(id=task_id)

    if task in sprint.tasks.all():
        sprint.tasks.remove(task)
        sprint.save()
    else:
        raise ValidationError("Task is not in the sprint.")


@transaction.atomic
def set_sprint_epic(sprint_id: int, epic_id: int) -> None:
    """
    Set the epic for the sprint.
    """
    sprint = Sprint.objects.select_for_updae().get(id=sprint_id)
    epic = Epic.objects.get(id=epic_id)

    sprint.epic = epic
    sprint.save()
