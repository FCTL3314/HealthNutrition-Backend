from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.decorators import order_queryset
from api.v1.users.constants import USERS_ORDERING
from api.v1.users.docs import email_verification_view_docs, verify_email_view_docs
from api.v1.users.paginators import UserPageNumberPagination
from api.v1.users.serializers import (
    CurrentUserSerializer,
    EmailVerificationSerializer,
    UserVerificationSerializer,
)
from api.v1.users.services.email_verification import (
    EmailVerifierService,
    EVSenderService,
)


class UserViewSet(DjoserUserViewSet):
    pagination_class = UserPageNumberPagination

    @order_queryset(*USERS_ORDERING)
    def get_queryset(self):
        return super().get_queryset()


@email_verification_view_docs()
class EmailVerificationCreateView(CreateAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        return EVSenderService(
            self.serializer_class,
            request.user,
        ).execute()


@verify_email_view_docs()
class VerifyEmailUpdateView(CreateAPIView):
    serializer_class = UserVerificationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return EmailVerifierService(
            self.serializer_class,
            CurrentUserSerializer,
            request.user,
            request.data,
        ).execute()
