from http import HTTPStatus

from accounts.services.auth import require_permission
from django.http import Http404, HttpRequest, HttpResponse
from ninja import Path, Router
from ninja.pagination import paginate
from tasks.api.schemas import PathDate, TaskSchemaIn, TaskSchemaOut
from tasks.api.security import JWTAuth
from tasks.enums import TaskStatus
from tasks.services import task as task_service

api_router = Router(tags=["tasks"], auth=JWTAuth())

# Example of using ModelSchema
#
# @api_router.get("/", response=list[TaskModelSchemaOut])
# def list_tasks(request):
#     return [
#         TaskModelSchemaOut(
#             title="Mock Task",
#             description="Mock Description",
#         )
#     ]


@paginate
@api_router.get("/", response=list[TaskSchemaOut])
def list_tasks(request: HttpRequest):
    return task_service.list_tasks()


@api_router.post("/", response={HTTPStatus.CREATED: TaskSchemaOut})
@require_permission("tasks.add_task")
def create_task(request: HttpRequest, task_in: TaskSchemaIn):
    creator = request.user
    return task_service.create_task(creator, **task_in.dict())


@api_router.get("/{int:task_id}/", response=TaskSchemaOut)
def get_task(request: HttpRequest, task_id: int):
    task = task_service.get_task(task_id)

    if task is None:
        raise Http404("Task not found")

    return task


@api_router.put("/{int:task_id}/", response={HTTPStatus.OK: TaskSchemaOut})
def update_task(request: HttpRequest, task_id: int, task_in: TaskSchemaIn):
    task = task_service.update_task(task_id, **task_in.dict())

    if task is None:
        raise Http404("Task not found")

    return task


@api_router.delete("/{int:task_id}/", response={HTTPStatus.NO_CONTENT: None})
def delete_task(request: HttpRequest, task_id: int):
    task = task_service.delete_task(task_id)

    if task is None:
        raise Http404("Task not found")

    return task


@api_router.get("/archive/{year}/{month}/{day}", response=list[TaskSchemaOut])
@paginate
def archived_tasks(request: HttpRequest, created_at: PathDate = Path(...)):
    return task_service.search_tasks(created_at=created_at.value(), status=TaskStatus.ARCHIVED.value)
