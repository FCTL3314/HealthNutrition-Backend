from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from api.v1.users.constants import EMAIL_SENDING_SECONDS_INTERVAL
from api.v1.users.models import EmailVerification


class BaseEmailSendingIntervalService(ABC):
    @abstractmethod
    def calculate_next_sending_datetime(self, user) -> datetime:
        ...


class EmailSendingIntervalService(BaseEmailSendingIntervalService):
    def calculate_next_sending_datetime(self, user) -> datetime:
        latest_verification = EmailVerification.objects.last_sent(user)
        sending_interval = timedelta(seconds=EMAIL_SENDING_SECONDS_INTERVAL)
        return latest_verification.created_at + sending_interval
