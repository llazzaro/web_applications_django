from datetime import date

from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from tasks import services
from tasks.mixins import SprintTaskWithinRangeMixin
from tasks.models import Task


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
    tasks = services.get_tasks_by_date(by_date)
    context = {"tasks": tasks}
    return render(request=request, template_name="task_list.html", context=context)
