from urllib.request import Request

from django.contrib import admin
from django.db.models import QuerySet
from tasks.models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "status",
        "owner",
        "owner",
        "created_at",
        "updated_at",
    )
    list_filter = ("status",)
    search_fields = ("title", "description", "created_at", "updated_at")

    actions = [
        "mark_as_done",
        "mark_as_in_progress",
        "mark_as_unassigned",
        "mark_as_archived",
    ]

    def mark_as_done(self, request: Request, queryset: QuerySet) -> None:
        queryset.update(status="DONE")

    def mark_as_in_progress(self, request: Request, queryset: QuerySet) -> None:
        queryset.update(status="IN PROGRESS")

    def mark_as_unassigned(self, request: Request, queryset: QuerySet) -> None:
        queryset.update(status="UNASSIGNED")

    def mark_as_archived(self, request: Request, queryset: QuerySet) -> None:
        queryset.update(status="ARCHIVED")

    def has_change_permission(self, request: Request, obj=None):
        if request.user.has_perm("tasks.change_task"):
            return True
        return False

    def has_add_permission(self, request):
        if request.user.has_perm("tasks.add_task"):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.has_perm("tasks.delete_task"):
            return True
        return False

    mark_as_done.short_description = "Mark selected tasks as done"
    mark_as_in_progress.short_description = "Mark selected tasks as in progress"
    mark_as_unassigned.short_description = "Mark selected tasks as unassigned"
    mark_as_archived.short_description = "Mark selected tasks as archived"


admin.site.register(Task, TaskAdmin)
