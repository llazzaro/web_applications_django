from datetime import datetime


class DateConverter:
    regex = "[0-9]{4}-[0-9]{2}-[0-9]{2}"

    def to_python(self, value) -> datetime:
        return datetime.strptime(value, "%Y-%m-%d")

    def to_url(self, object) -> str:
        return object.strftime("%Y-%m-%d")
