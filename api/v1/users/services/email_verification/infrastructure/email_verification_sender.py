from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from api.common.services import AbstractService
from api.v1.users.models import EmailVerification
from api.v1.users.services.data_transfer import EVAdapter
from api.v1.users.services.email_verification.domain.email_sending_availability import (
    EVAvailabilityResponse,
    EVAvailabilityService,
    EVAvailabilityStatus,
)
from api.v1.users.services.email_verification.domain.next_sending_time import (
    EVNextSendingTimeService,
)
from api.v1.users.services.email_verification.domain.sending_interval_checker import (
    EVSendingIntervalCheckerService,
)
from api.v1.users.tasks import send_verification_email

SENDING_LIMIT_REACHED_MSG = "Sending limit reached."


class EVSenderService(AbstractService):
    def __init__(
        self, serializer_class: type[Serializer], user: AbstractUser | AbstractBaseUser
    ):
        self._serializer_class = serializer_class
        self._user = user
        self._sending_availability_service = EVAvailabilityService(
            EVAdapter.to_dto(EmailVerification.objects.last_sent(self._user.id)),
            EVNextSendingTimeService(),
            EVSendingIntervalCheckerService(),
        )

    def execute(self) -> Response:
        response = self._sending_availability_service.execute()
        return self.handle_availability_response(response)

    def handle_availability_response(
        self, response: EVAvailabilityResponse
    ) -> Response:
        match response.status:
            case EVAvailabilityStatus.CAN_BE_SENT:
                email_verification = self._send()
                return self.email_sent_response(email_verification)
            case EVAvailabilityStatus.SENDING_LIMIT_REACHED:
                return self.sending_limit_reached_response(response.retry_after)

    def _send(self) -> EmailVerification:
        email_verification = EmailVerification.objects.create(user_id=self._user.id)
        send_verification_email.delay(object_id=email_verification.id)
        return email_verification

    def email_sent_response(self, email_verification: EmailVerification):
        return Response(
            self._serializer_class(email_verification).data,
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    def sending_limit_reached_response(retry_after: datetime):
        return Response(
            {
                "detail": SENDING_LIMIT_REACHED_MSG,
                "retry_after": retry_after,
            },
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        )
