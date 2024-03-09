from ninja import NinjaAPI
from tasks.api.tasks import api_router as tasks_router

api = NinjaAPI()

api.add_router("tasks/", tasks_router)
