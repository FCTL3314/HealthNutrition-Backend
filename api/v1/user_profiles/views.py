from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from api.responses import APIResponse
from api.v1.user_profiles.serializers import UserProfileSerializer
from api.v1.user_profiles.services.infrastructure.user_profile_update import (
    UserProfileUpdateService,
)


class UserProfileUpdateView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user.profile  # noqa

    def update(self, request: Request, *args, **kwargs) -> Response | APIResponse:
        return UserProfileUpdateService(
            self.get_object(),
            self.get_serializer_class(),
            request.data,
            kwargs.get("partial", False),
        ).execute()
