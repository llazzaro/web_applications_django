from collections import Counter

from django import template

register = template.Library()


@register.simple_tag
def task_summary(sprint):
    # Getting all tasks associated with this sprint
    tasks = sprint.tasks.all()

    # Counting tasks with each status
    task_statuses = [task.status for task in tasks]
    summary = Counter(task_statuses)

    return summary
