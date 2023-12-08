from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.common.djoser import extended_settings
from api.responses import APIResponse
from api.v1.users.constants import USERS_ORDERING
from api.v1.users.docs import (
    user_change_email_view_docs,
    user_email_verifier_view_docs,
    user_send_email_verification_view_docs,
)
from api.v1.users.paginators import UserPageNumberPagination
from api.v1.users.serializers import (
    CurrentUserSerializer,
    EmailVerificationSerializer,
    UserChangeEmailSerializer,
    UserVerificationSerializer,
    UIDAndTokenSerializer,
)
from api.v1.users.services.infrastructure.user_change_email import (
    UserChangeEmailService,
)
from api.v1.users.services.infrastructure.user_email_verification import (
    EVSenderService,
    UserEmailVerifierService,
)
from api.v1.users.services.infrastructure.user_update import UserUpdateService

User = get_user_model()


class UserViewSet(DjoserUserViewSet):
    pagination_class = UserPageNumberPagination

    def get_permissions(self):
        super().get_permissions()
        if self.action == "me":
            self.permission_classes = extended_settings.PERMISSIONS.current_user
        return super(DjoserUserViewSet, self).get_permissions()

    def get_queryset(self) -> QuerySet[User]:
        queryset = super().get_queryset()
        return queryset.order_by(*USERS_ORDERING)

    def update(self, request: Request, *args, **kwargs) -> Response | APIResponse:
        return UserUpdateService(
            self.get_object(),
            self.get_serializer_class(),
            request.data,
            kwargs.get("partial", False),
        ).execute()


@user_send_email_verification_view_docs()
class UserChangeEmailView(APIView):
    serializer_class = UserChangeEmailSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs) -> APIResponse:
        return UserChangeEmailService(
            self.serializer_class,
            request.user,
            request.data,
        ).execute()


@user_change_email_view_docs()
class UserSendEmailVerificationView(CreateAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request: Request, *args, **kwargs) -> APIResponse:
        return EVSenderService(
            self.serializer_class,
            request.user,
        ).execute()


@user_email_verifier_view_docs()
class UserEmailVerifierView(APIView):
    serializer_class = UserVerificationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs) -> APIResponse:
        return UserEmailVerifierService(
            self.serializer_class,
            CurrentUserSerializer,
            request.user,
            request.data,
        ).execute()


class CheckUIDAndToken(APIView):
    @staticmethod
    def post(request: Request) -> Response:
        serializer = UIDAndTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(status=HTTPStatus.NOT_FOUND, data=serializer.errors)
