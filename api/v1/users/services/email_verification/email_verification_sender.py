from abc import ABC, abstractmethod

from rest_framework import status
from rest_framework.response import Response

from api.v1.users.services.email_verification.email_sending_interval import (
    BaseEmailSendingIntervalService,
)
from api.v1.users.tasks import send_verification_email


class BaseEmailVerificationSenderService(ABC):
    def __init__(
        self,
        sending_interval_service: BaseEmailSendingIntervalService,
        serializer_class,
    ):
        self._sending_interval_service = sending_interval_service
        self._serializer_class = serializer_class

    @abstractmethod
    def send(self, user) -> Response:
        ...


class EmailVerificationSenderService(BaseEmailVerificationSenderService):
    def send(self, user) -> Response:
        if user.is_verification_sending_interval_passed():
            verification = user.create_email_verification()
            send_verification_email.delay(object_id=verification.id)
            serializer = self._serializer_class(verification)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return self._sending_limit_reached_response(user)

    def _sending_limit_reached_response(self, user) -> Response:
        response = {
            "detail": "Sending limit reached.",
            "retry_after": self._sending_interval_service.calculate_next_sending_datetime(
                user
            ),
        }
        return Response(response, status=status.HTTP_429_TOO_MANY_REQUESTS)
