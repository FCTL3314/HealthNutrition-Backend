from djoser.views import UserViewSet as DjoserUserViewSet
from drf_spectacular.utils import extend_schema_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from api.decorators import order_queryset
from api.v1.users.constants import USERS_ORDERING
from api.v1.users.docs import EMAIL_VERIFICATION_VIEW_DOCS, VERIFY_EMAIL_VIEW_DOCS
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


@extend_schema_view(**EMAIL_VERIFICATION_VIEW_DOCS)
class EmailVerificationCreateView(CreateAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        return EVSenderService(
            self.serializer_class,
            request.user,
        ).execute()


@extend_schema_view(**VERIFY_EMAIL_VIEW_DOCS)
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
