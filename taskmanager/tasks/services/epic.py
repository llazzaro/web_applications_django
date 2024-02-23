from tasks.models import Epic


def get_epic_by_id(epic_id: int) -> Epic:
    try:
        return Epic.objects.get(id=epic_id)
    except Epic.DoesNotExist:
        return None
