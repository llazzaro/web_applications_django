import time

from tasks.tasks_logger import get_logger

logger = get_logger(__name__)


class RequestTimeMiddleware:
    """
    Middleware that logs the time a request started
    """

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time

        logger.info(f"Request to {request.path} took {duration:.2f} seconds.")

        return response
