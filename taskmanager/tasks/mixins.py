from django.http import HttpResponseForbidden


class UserIsOwnerMixin:
    def user_is_owner(self, obj):
        return self.request.user == obj.owner

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if not self.user_is_owner(obj):
            return HttpResponseForbidden("You don't have permission to do this.")
        return super().dispatch(request, *args, **kwargs)
