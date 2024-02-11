from django.core.cache import cache
from django.http import HttpRequest


def feature_flags(request: HttpRequest) -> dict:
    user = request.user
    flags = {
        "is_priority_feature_enabled": False,
    }

    if user.is_authenticated:
        cache_key = f"user_{user.id}_is_priority_feature"
        if_priority_feature_enabled = cache.get(cache_key)

        if if_priority_feature_enabled is None:
            if_priority_feature_enabled = user.groups.filter(name="Task Prioritization Beta Testers").exists()
            cache.set(cache_key, if_priority_feature_enabled, timeout=300)  # Storing in cache for 5 minutes.

        flags["is_priority_feature_enabled"] = if_priority_feature_enabled

    return flags
