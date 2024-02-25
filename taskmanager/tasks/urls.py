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
    path("", TemplateView.as_view(template_name="tasks/home.html"), name="task-home"),
    path("help/", TemplateView.as_view(template_name="tasks/help.html"), name="help"),
    path("", TaskListView.as_view(), name="task-list"),
    path("new/", TaskCreateView.as_view(), name="task-create"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task-detail"),
    path("<int:pk>/edit/", TaskUpdateView.as_view(), name="task-edit"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
    path("<yyyymmdd:start_date>/", views.task_by_date, name="task-list-by-date"),
    path("sprint/add_task/<int:pk>/", views.create_task_on_sprint, name="task-add-on-sprint"),
    path("contact/", views.ContactFormView.as_view(), name="contact"),
    path("contact-success/", TemplateView.as_view(template_name="tasks/contact_success.html"), name="contact-success"),
]
