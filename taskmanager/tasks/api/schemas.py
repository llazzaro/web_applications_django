from ninja import Field, Schema


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
