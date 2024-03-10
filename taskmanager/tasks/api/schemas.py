import datetime

from ninja import Field, Schema
from tasks.enums import TaskStatus


class TaskSchemaIn(Schema):
    title: str = Field(..., example="Test Task Title")
    description: str = Field(..., example="Test Task Description")

    class Meta:
        description = "The data required to create a new task."


class TaskSchemaOut(TaskSchemaIn):
    id: int = Field(..., example=1)

    class Meta:
        description = "The data returned when a new task is created."
        fields_optional = ["id"]


class PathDate(Schema):
    year: int = Field(..., ge=2024)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)

    class Meta:
        description = "The date in the path."

    def value(self):
        return datetime.date(self.year, self.month, self.day)


class TaskFilterSchema(Schema):
    title: str | None
    tatus: TaskStatus | None

    class Meta:
        description = "The filter for tasks."
