from datetime import date

from django.http import Http404, HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView
from rest_framework import status
from tasks.exceptions import TaskAlreadyClaimedException
from tasks.mixins import SprintTaskWithinRangeMixin
from tasks.models import Task
from tasks.services import task as task_service
from tasks.services.task import claim_task


class TaskListView(ListView):
    model = Task
    template_name = "task_list.html"
    context_object_name = "tasks"


class TaskDetailView(ListView):
    model = Task
    template_name = "task_detail.html"
    context_object_name = "task"


class TaskCreateView(SprintTaskWithinRangeMixin, ListView):
    model = Task
    template_name = "task_form.html"
    fields = ("name", "description", "start_date", "end_date")

    def get_success_url(self):
        return reverse("task-detail", kwargs={"pk": self.object.pk})


class TaskUpdateView(SprintTaskWithinRangeMixin, ListView):
    model = Task
    template_name = "task_form.html"
    fields = ("name", "description", "start_date", "end_date")

    def get_success_url(self):
        return reverse("task-detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(ListView):
    model = Task
    template_name = "task_confirm_delete.html"

    def get_success_url(self):
        return reverse("task-list")


def task_by_date(request: HttpRequest, by_date: date):
    tasks = task_service.get_tasks_by_date(by_date)
    context = {"tasks": tasks}
    return render(request=request, template_name="task_list.html", context=context)


def create_task_on_sprint(request: HttpRequest, sprint_id: int):
    if request.method == "POST":
        task_data: dict[str, str] = {
            "title": request.POST["title"],
            "description": request.POST.get("description", ""),
            "status": request.POST.get("status", "UNASSIGNED"),
        }
        task = task_service.create_task_and_add_to_sprint(
            task_data=task_data, sprint_id=sprint_id, creator=request.user
        )
        return redirect("task-detail", task_id=task.id)

    return Http404("Not found.")


def claim_task_view(request: HttpRequest, task_id: int):
    user_id = request.user.id

    try:
        claim_task(user_id, task_id)
        return JsonResponse({"message": "Task claimed successfully."})
    except Task.DoesNotExist:
        return HttpResponse("Task does not exist.", status=status.HTTP_404_NOT_FOUND)
    except TaskAlreadyClaimedException:
        return HttpResponse("Task already claimed or completed.", status=status.HTTP_409_CONFLICT)

    task = Task.objects.get(id=task_id)
    task.owner = request.user
    task.save()
    return redirect("task-detail", task_id=task.id)
