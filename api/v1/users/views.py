from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.v1.users.constants import USERS_ORDERING
from api.v1.users.docs import email_verification_view_docs, verify_email_view_docs
from api.v1.users.paginators import UserPageNumberPagination
from api.v1.users.serializers import (
    CurrentUserSerializer,
    EmailVerificationSerializer,
    UserVerificationSerializer,
)
from api.v1.users.services.infrastructure.email_verification import (
    EVSenderService,
    UserEmailVerifierService,
)


class UserViewSet(DjoserUserViewSet):
    pagination_class = UserPageNumberPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by(*USERS_ORDERING)


@email_verification_view_docs()
class UserSendEmailVerificationView(CreateAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        return EVSenderService(
            self.serializer_class,
            request.user,
        ).execute()


@verify_email_view_docs()
class UserEmailVerifierView(APIView):
    serializer_class = UserVerificationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return UserEmailVerifierService(
            self.serializer_class,
            CurrentUserSerializer,
            request.user,
            request.data,
        ).execute()
