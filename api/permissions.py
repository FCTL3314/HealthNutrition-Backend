from rest_framework.permissions import SAFE_METHODS, IsAdminUser


class IsAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        if view.action not in SAFE_METHODS:
            return super().has_permission(request, view)
        return True
