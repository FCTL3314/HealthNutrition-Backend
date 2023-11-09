from rest_framework.permissions import SAFE_METHODS, IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView


class IsAdminOrReadOnly(IsAdminUser):
    """
    Allows to create, update, and delete objects if
    the user is an administrator.
    """

    def has_permission(self, request: Request, view: APIView) -> bool:
        return bool(
            request.method in SAFE_METHODS or super().has_permission(request, view)
        )
