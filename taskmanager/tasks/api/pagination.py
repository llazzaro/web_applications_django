from typing import Any

from django.db.models import QuerySet
from ninja import Schema
from ninja.pagination import PaginationBase


class TaskManagerPagination(PaginationBase):
    class Input(Schema):
        skip_records: int

    class Output(Schema):
        items: list[Any]
        count: int
        page_size: int

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Any,
        **params: Any,
    ) -> Any:
        skip_records = pagination.skip_records
        page_size = 5
        return {
            "data": queryset[skip_records : skip_records + page_size],
            "count": queryset.count(),
            "page_size": page_size,
        }
