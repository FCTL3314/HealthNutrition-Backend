from dependencies import Injector

from api.v1.users.serializers import EmailVerificationSerializer
from api.v1.users.services.email_verification.email_sending_interval import (
    EmailSendingIntervalService,
)
from api.v1.users.services.email_verification.email_verification_sender import (
    EmailVerificationSenderService,
)


class EmailVerificationSenderDependencies(Injector):
    email_verification_sender_service = EmailVerificationSenderService
    sending_interval_service = EmailSendingIntervalService
    serializer_class = EmailVerificationSerializer
