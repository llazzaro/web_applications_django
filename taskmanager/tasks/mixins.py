from django.http import HttpResponseBadRequest


class SprintTaskWithinRangeMixin:
    """
    Mixin to check if the task is within the sprint range.
    """

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object() if hasattr(self, "get_object") else None
        sprint_id = request.POST.get("spring")

        if sprint_id:
            if task or request.method == "POST":
                if not can_add_task_to_sprint(task, sprint_id):
                    return HttpResponseBadRequest("Task's creation date is out of sprint range.")

        return super().dispatch(request, *args, **kwargs)
