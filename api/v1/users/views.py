from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
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
)
from api.v1.users.services.infrastructure.user_change_email import (
    UserChangeEmailService,
)
from api.v1.users.services.infrastructure.user_email_verification import (
    EVSenderService,
    UserEmailVerifierService,
)

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
