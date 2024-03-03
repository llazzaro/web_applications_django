from collections import defaultdict
from datetime import date

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView
from rest_framework import status
from tasks.exceptions import TaskAlreadyClaimedException
from tasks.forms import ContactForm, EpicFormSet, TaskForm
from tasks.mixins import SprintTaskWithinRangeMixin
from tasks.models import Epic, Sprint, Task
from tasks.services import epic as epic_service
from tasks.services import sprint as sprint_service
from tasks.services import task as task_service
from tasks.services.email import send_contact_email
from tasks.services.task import claim_task


## TASKS
class TaskListView(PermissionRequiredMixin, ListView):
    model = Task
    permission_required = (
        "tasks.view_task",
        "tasks.custom_task",
    )
    login_url = reverse_lazy("accounts:login")
    template_name = "task_list.html"
    context_object_name = "tasks"


class TaskDetailView(DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "tasks/task_form.html"
    context_object_name = "task"
    form_class = TaskForm

    def get_success_url(self):
        self.object.save()
        return reverse("tasks:task-detail", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskUpdateView(PermissionRequiredMixin, SprintTaskWithinRangeMixin, ListView):
    model = Task
    template_name = "task_form.html"
    fields = ("name", "description", "start_date", "end_date")

    def get_success_url(self):
        return reverse("task-detail", kwargs={"pk": self.object.pk})

    def has_permission(self):
        if not (has_general_permission := super().has_permission()):
            return False

        task_id = self.kwargs.get("pk")
        task = get_object_or_404(Task, id=task_id)
        is_creator_or_owner = task.creator == self.request.user or task.owner == self.request.user

        return has_general_permission and is_creator_or_owner


class TaskDeleteView(ListView):
    model = Task
    template_name = "task_confirm_delete.html"

    def get_success_url(self):
        return reverse("task-list")


class ContactFormView(FormView):
    template_name = "tasks/contact_form.html"
    form_class = ContactForm
    success_url = reverse_lazy("tasks:contact-success")

    def form_valid(self, form: ContactForm) -> HttpResponseRedirect:
        subject = form.cleaned_data["subject"]
        message = form.cleaned_data["message"]
        from_email = form.cleaned_data["from_email"]

        send_contact_email(
            subject=subject, message=message, from_email=from_email, to_email="cardenasmatias.1990@gmail.com"
        )

        return super().form_valid(form)


## SPRINTS


class SprintListView(ListView):
    model = Sprint
    template_name = "sprints.html"
    context_object_name = "sprints"


class SprintDetailView(ListView):
    model = Sprint
    template_name = "sprint_detail.html"
    context_object_name = "sprint"


def task_home(request: HttpRequest):
    tasks = Task.objects.filter(status__in=["UNASSIGNED", "IN_PROGRESS", "DONE", "ARCHIVED"])

    context = defaultdict(list)

    for task in tasks:
        if task.status == "UNASSIGNED":
            context["unassigned_tasks"].append(task)
        elif task.status == "IN_PROGRESS":
            context["in_progress_tasks"].append(task)
        elif task.status == "DONE":
            context["done_tasks"].append(task)
        elif task.status == "ARCHIVED":
            context["archived_tasks"].append(task)

    return render(request, "tasks/home.html", context)


def sprint_home(request: HttpRequest):
    context = sprint_service.get_grouped_sprints()
    return render(request, "tasks/sprints.html", context)


def task_by_date(request: HttpRequest, by_date: date):
    tasks = task_service.get_tasks_by_date(by_date)
    context = {"tasks": tasks}
    return render(request=request, template_name="task_list.html", context=context)


@permission_required("tasks.add_task")
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


def create_sprint(request: HttpRequest):
    if request.method == "POST":
        sprint_data = {
            "name": request.POST["name"],
            "description": request.POST.get("description", ""),
            "start_date": request.POST["start_date"],
            "end_date": request.POST["end_date"],
        }
        sprint = sprint_service.create_sprint(sprint_data, request.user)
        return redirect("sprint-detail", sprint_id=sprint.id)

    return Http404("Not found.")


def remove_task_from_sprint(request: HttpRequest, task_id: int, sprint_id: int):
    try:
        sprint_service.remove_task_from_sprint(task_id, sprint_id)
        return JsonResponse({"message": "Task removed from sprint successfully."})
    except Task.DoesNotExist:
        return HttpResponse("Task does not exist.", status=status.HTTP_404_NOT_FOUND)
    except Sprint.DoesNotExist:
        return HttpResponse("Sprint does not exist.", status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return HttpResponse(str(e), status=status.HTTP_409_CONFLICT)


def set_sprint_epic(request: HttpRequest, sprint_id: int, epic_id: int):
    try:
        sprint_service.set_sprint_epic(sprint_id, epic_id)
        return JsonResponse({"message": "Sprint epic set successfully."})
    except Sprint.DoesNotExist:
        return HttpResponse("Sprint does not exist.", status=status.HTTP_404_NOT_FOUND)
    except Epic.DoesNotExist:
        return HttpResponse("Epic does not exist.", status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return HttpResponse(str(e), status=status.HTTP_409_CONFLICT)


def manage_epic_tasks(request: HttpRequest, epic_id: int) -> HttpResponse:
    epic = epic_service.get_epic_by_id(epic_id)

    if not epic:
        raise Http404("Epic does not exist.")

    if request.method == "POST":
        formset = EpicFormSet(request.POST, queryset=task_service.get_tasks_by_epic(epic_id))

        if formset.is_valid():
            tasks = formset.save(commit=False)
            task_service.save_tasks_for_epic(epic, tasks)
            formset.save_m2m()
            return redirect("tasks:task-list")
    else:
        formset = EpicFormSet(queryset=task_service.get_tasks_by_epic(epic_id))

    return render(
        request=request,
        template_name="tasks/manage_epic.html",
        context={"formset": formset, "epic": epic},
    )
