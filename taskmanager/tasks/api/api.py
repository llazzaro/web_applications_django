from django.core.exceptions import ObjectDoesNotExist
from ninja import NinjaAPI
from tasks.api.security import APITokenAuth, JWTAuth
from tasks.api.tasks import api_router as tasks_router

api = NinjaAPI(version="v1", auth=[JWTAuth()])

# If we would have different authentication for APIs within the project,
# we could apply the authentication to the specific routers.

api.add_router("tasks/", tasks_router)


@api.exception_handler(ObjectDoesNotExist)
def on_object_does_not_exist(request, exc):
    return 404, {"message": "Object not found"}
