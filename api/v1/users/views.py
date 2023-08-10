from rest_framework.generics import CreateAPIView, UpdateAPIView

from api.v1.users.dependencies import EmailVerificationSenderDependencies
from api.v1.users.services.email_verification.user_email_verifier import (
    UserEmailVerifierService,
)


class EmailVerificationCreateAPIView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        return (
            EmailVerificationSenderDependencies.email_verification_sender_service.send(
                request.user
            )
        )


class VerifyUserUpdateAPIView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        return UserEmailVerifierService(request.user, request.data).verify()
