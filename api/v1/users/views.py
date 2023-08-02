from rest_framework.generics import CreateAPIView, UpdateAPIView

from api.v1.users.services import EmailVerificationSenderService, UserEmailVerifierService


class EmailVerificationCreateAPIView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        return EmailVerificationSenderService(request).send()


class VerifyUserUpdateAPIView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        return UserEmailVerifierService(request).verify()
