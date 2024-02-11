from django.urls import path, register_converter
from django.views.generic import TemplateView
from tasks import views
from tasks.converters import DateConverter
from tasks.views import (
    TaskCreateView,
    TaskDeleteView,
    TaskDetailView,
    TaskListView,
    TaskUpdateView,
)

app_name = "tasks"

register_converter(DateConverter, "yyyymmdd")

urlpatterns = [
    path("", TemplateView.as_view(template_name="tasks/home.html"), name="home"),
    path("help/", TemplateView.as_view(template_name="tasks/help.html"), name="help"),
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/new/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-edit"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("tasks/<yyyymmdd:start_date>/", views.task_by_date, name="task-list-by-date"),
    path("tasks/sprint/add_task/<int:pk>/", views.create_task_on_sprint, name="task-add-on-sprint"),
]
