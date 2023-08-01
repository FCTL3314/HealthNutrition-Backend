from rest_framework.generics import CreateAPIView, UpdateAPIView

from common.mixins import RequestDataValidationMixin
from users.serializers import VerifyUserSerializer
from users.services import EmailVerificationSender, UserEmailVerifier


class EmailVerificationCreateAPIView(CreateAPIView):
    def create(self, request, *args, **kwargs):
        sender_service = EmailVerificationSender(self.request.user, request)
        response = sender_service.send()
        return response


class VerifyUserUpdateAPIView(RequestDataValidationMixin, UpdateAPIView):
    serializer_class = VerifyUserSerializer

    def update(self, request, *args, **kwargs):
        self.validate_request_data()

        verifier_service = UserEmailVerifier(
            self.request.user, request, request.data["code"]
        )
        response = verifier_service.verify()
        return response
