from rest_framework.generics import CreateAPIView, UpdateAPIView

from api.mixins import RequestDataValidationMixin
from api.v1.users.mixins import EmailVerificationMixin
from api.v1.users.serializers import (SendVerificationEmailSerializer,
                                      VerifyUserSerializer)
from api.v1.users.services import EmailVerificationSender, UserEmailVerifier


class EmailVerificationCreateAPIView(
    RequestDataValidationMixin, EmailVerificationMixin, CreateAPIView
):
    serializer_class = SendVerificationEmailSerializer

    def create(self, request, *args, **kwargs):
        self.validate_request_data()

        sender_service = EmailVerificationSender(self.get_user(), request)
        response = sender_service.send()
        return response


class VerifyUserUpdateAPIView(
    RequestDataValidationMixin, EmailVerificationMixin, UpdateAPIView
):
    serializer_class = VerifyUserSerializer

    def update(self, request, *args, **kwargs):
        self.validate_request_data()

        verifier_service = UserEmailVerifier(
            self.get_user(), request, request.data["code"]
        )
        response = verifier_service.verify()
        return response
