from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from api.common.time_providers import AbstractTimeProvider
from api.v1.users.constants import EV_SENDING_INTERVAL_TIMEDELTA
from api.v1.users.models import EmailVerification
from api.v1.users.services.data_transfer import EVAdapter, UserAdapter
from api.v1.users.services.email_verification import (
    EVAvailabilityService,
    EVAvailabilityStatus,
    EVNextSendingTimeService,
    EVSendingIntervalCheckerService,
)

User = get_user_model()


class TestNextSendingTimeCalculator:
    @pytest.mark.django_db
    def test_without_previous_sending(self, utc_time_provider: AbstractTimeProvider):
        next_sending_datetime = EVNextSendingTimeService(None).execute()

        assert next_sending_datetime == pytest.approx(
            utc_time_provider.now,
            abs=self.timedelta_approx,
        )

    @pytest.mark.django_db
    def test_with_previous_sending(
        self,
        email_verification: EmailVerification,
        utc_time_provider: AbstractTimeProvider,
    ):
        next_sending_datetime = EVNextSendingTimeService(
            EVAdapter().to_dto(email_verification)
        ).execute()

        assert next_sending_datetime == pytest.approx(
            email_verification.created_at + EV_SENDING_INTERVAL_TIMEDELTA,
            abs=self.timedelta_approx,
        )

    @property
    def timedelta_approx(self):
        return timedelta(seconds=1, microseconds=100)


class TestSendingIntervalCheckerService:
    @pytest.mark.django_db
    def test_can_be_sent(self, utc_time_provider: AbstractTimeProvider):
        assert EVSendingIntervalCheckerService(
            EVNextSendingTimeService(None),
        ).execute()

    @pytest.mark.django_db
    def test_cannot_be_sent(
        self,
        email_verification: EmailVerification,
        utc_time_provider: AbstractTimeProvider,
    ):
        assert not EVSendingIntervalCheckerService(
            EVNextSendingTimeService(
                EVAdapter().to_dto(email_verification),
            )
        ).execute()


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_verified, previous_sending, expected_status",
    [
        (
            False,
            False,
            EVAvailabilityStatus.CAN_BE_SENT,
        ),
        (
            False,
            True,
            EVAvailabilityStatus.SENDING_LIMIT_REACHED,
        ),
        (
            True,
            True,
            EVAvailabilityStatus.ALREADY_VERIFIED,
        ),
    ],
)
def test_email_sending_availability_service(
    is_verified: bool,
    previous_sending: bool,
    expected_status: EVAvailabilityStatus,
):
    user_dto = UserAdapter().to_dto(mixer.blend("users.User", is_verified=is_verified))
    ev_dto = (
        EVAdapter().to_dto(mixer.blend("users.EmailVerification"))
        if previous_sending
        else None
    )

    service = EVAvailabilityService(
        user_dto,
        EVSendingIntervalCheckerService(EVNextSendingTimeService(ev_dto)),
    )

    assert service.execute() == expected_status


if __name__ == "__main__":
    pytest.main()