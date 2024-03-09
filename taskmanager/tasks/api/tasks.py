from django.http import HttpRequest
from ninja import Router
from tasks.api.schemas import TaskSchemaIn, TaskSchemaOut

api_router = Router(tags=["tasks"])

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


@api_router.get("/", response=list[TaskSchemaOut])
def list_tasks(request: HttpRequest):
    return {
        "results": [
            TaskSchemaOut(
                **{
                    "id": 1,
                    "title": "Test Task Title",
                },
            )
        ]
    }


@api_router.post("/", response=TaskSchemaOut)
def create_task(request: HttpRequest, task_in: TaskSchemaIn):
    return TaskSchemaOut(id=1, **task_in.dict())
