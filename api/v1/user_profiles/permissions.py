from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from api.v1.user_profiles.models import UserProfile


class IsProfileOwner(BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, profile: UserProfile
    ) -> bool:
        return bool(profile.user.id == request.user.id)
