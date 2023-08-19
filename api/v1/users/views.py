from rest_framework.generics import CreateAPIView, UpdateAPIView

from api.v1.users.serializers import (
    CurrentUserSerializer,
    EmailVerificationSerializer,
    UserVerificationSerializer,
)
from api.v1.users.services.email_verification import (
    EmailVerifierService,
    EVSenderService,
)


class EmailVerificationCreateAPIView(CreateAPIView):
    serializer_class = EmailVerificationSerializer

    def create(self, request, *args, **kwargs):
        return EVSenderService(
            self.serializer_class,
            request.user,
        ).execute()


class VerifyUserUpdateAPIView(UpdateAPIView):
    serializer_class = UserVerificationSerializer

    def update(self, request, *args, **kwargs):
        return EmailVerifierService(
            self.serializer_class,
            CurrentUserSerializer,
            request.user,
            request.data,
        ).execute()
