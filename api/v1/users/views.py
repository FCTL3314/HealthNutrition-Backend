from rest_framework.generics import CreateAPIView, UpdateAPIView

from api.v1.users.serializers import EmailVerificationSerializer
from api.v1.users.services.email_verification.domain.user_email_verifier import (
    UserEmailVerifierService,
)
from api.v1.users.services.email_verification.infrastructure.email_sender import (
    EVSenderService,
)


class EmailVerificationCreateAPIView(CreateAPIView):
    serializer_class = EmailVerificationSerializer

    def create(self, request, *args, **kwargs):
        return EVSenderService(
            self.serializer_class,
            request.user.id,
        ).execute()


class VerifyUserUpdateAPIView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        return UserEmailVerifierService(request.user, request.data).verify()
