from rest_framework.permissions import SAFE_METHODS, IsAdminUser


class IsAdminOrReadOnly(IsAdminUser):
    """
    Allows to create, update, and delete objects if
    the user is an administrator.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or super().has_permission(request, view)
        )
