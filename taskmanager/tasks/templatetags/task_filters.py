import markdown
from django import template
from django.db.models import Count, Q
from tasks.models import Comment, Task

register = template.Library()


@register.filter
def percent_complete(tasks):
    if tasks.exists():
        aggregation = tasks.aggregate(total=Count("id"), done=Count("id", filter=Q(status="DONE")))

        percent_done = (aggregation["done"] / aggregation["total"]) * 100

        return percent_done
    else:
        return 0


@register.filter
def markdown_to_html(comment: Comment):
    return markdown.markdown(comment.content, output_format="html5", extensions=["escape_html"])
