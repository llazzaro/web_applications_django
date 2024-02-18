from django.contrib.auth.models import User
from django.db import models

# Create your models here.

TASK_STATUS_CHOICES = [
    ("UNASSIGNED", "Unassigned"),
    ("IN PROGRESS", "In Progress"),
    ("DONE", "Done"),
    ("ARCHIVED", "Archived"),
]

TASK_PRIORITY_CHOICES = [
    ("LOW", "Low"),
    ("MEDIUM", "Medium"),
    ("HIGH", "High"),
]


class Epic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_epics")


class VersionMixin:
    version = models.IntegerField(default=0)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table_comment = "Holds comments for tasks."
        ordering = ["-created_at"]


class Task(VersionMixin, models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=False, default="")
    status = models.CharField(
        max_length=20,
        choices=TASK_STATUS_CHOICES,
        default="UNASSIGNED",
        db_comment="Can be UNASSIGNED, IN PROGRESS, DONE, or ARCHIVED",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tasks")
    owner = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="owned_tasks",
        blank=True,
        null=True,
    )
    epic = models.ForeignKey(Epic, on_delete=models.SET_NULL, related_name="tasks", blank=True, null=True)
    due_date = models.DateField(blank=True, null=True, db_comment="The date when the task is due.")
    version = models.IntegerField(default=0)
    priority = models.CharField(
        max_length=20,
        choices=TASK_PRIORITY_CHOICES,
        default="LOW",
        db_comment="Can be LOW, MEDIUM, or HIGH",
    )

    class Meta:
        db_table_comment = "Holds information about tasks."

        constraints = [
            models.CheckConstraint(
                check=models.Q(status__in=[s[0] for s in TASK_STATUS_CHOICES]),
                name="valid_status",
            ),
            models.CheckConstraint(
                check=models.Q(due_date__gt=models.F("created_at")),
                name="due_date_after_created_at",
            ),
        ]


class Sprint(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_sprints")
    tasks = models.ManyToManyField(Task, related_name="sprints", blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(end_date__gt=models.F("start_date")),
                name="end_date_after_start_date",
            ),
        ]
