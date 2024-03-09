from ninja import Field, ModelSchema
from tasks.models import Task


class TaskModelSchemaIn(ModelSchema):
    class Meta:
        model = Task
        fields = ["title", "description"]
        fields_optional = ["description"]


class TaskModelSchemaOut(ModelSchema):
    onwer: int | None = Field(None, title="Owner ID")

    class Meta:
        model = Task
        fields = ["title", "description"]
