from django import template
from django.db.models import Count
from tasks.models import Sprint

register = template.Library()


@register.simple_tag
def task_summary(sprint: Sprint):
    """
    Groups tasks by status and count each group
    """

    task_counts = sprint.tasks.values("status").annotate(count=Count("status")).order_by()

    summary = {item["status"]: item["count"] for item in task_counts}

    return summary


@register.simple_tag
def task_priority_summary(sprint: Sprint):
    """
    Groups tasks by priority and count each group
    """

    task_counts = sprint.tasks.values("priority").annotate(count=Count("priority")).order_by()

    summary = {item["priority"]: item["count"] for item in task_counts}

    return summary
