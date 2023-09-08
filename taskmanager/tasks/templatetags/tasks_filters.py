from django import template
from django.db.models import QuerySet

register = template.Library()


@register.filter
def percent_complete(tasks: QuerySet) -> float:
    total = tasks.count()
    if total == 0:
        return 0

    done = tasks.filter(status="DONE").count()
    return (done / total) * 100
