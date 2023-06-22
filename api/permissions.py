from rest_framework.permissions import IsAdminUser


class IsAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        if view.action in ("create", "update", "destroy"):
            return super().has_permission(request, view)
        return True
