import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

from api.base.time_providers import TimeProviderProto
from api.utils.time import is_datetime_attrs_equal
from api.v1.users.constants import EV_SENDING_INTERVAL_TIMEDELTA
from api.v1.users.models import EmailVerification
from api.v1.users.services.converters import EVConverter, UserConverter
from api.v1.users.services.domain.email_verification import (
    EVAvailabilityStatus,
    get_ev_next_sending_datetime,
    get_ev_sending_availability_status,
    is_ev_sending_interval_passed,
)

User = get_user_model()


class TestNextSendingTimeCalculator:
    @pytest.mark.django_db
    def test_without_previous_sending(self, utc_time_provider: TimeProviderProto):
        next_sending_datetime = get_ev_next_sending_datetime(None)

        assert is_datetime_attrs_equal(
            (
                next_sending_datetime,
                utc_time_provider.now(),
            )
        )

    @pytest.mark.django_db
    def test_with_previous_sending(
        self,
        email_verification: EmailVerification,
    ):
        next_sending_datetime = get_ev_next_sending_datetime(email_verification)

        assert is_datetime_attrs_equal(
            (
                next_sending_datetime,
                email_verification.created_at + EV_SENDING_INTERVAL_TIMEDELTA,
            )
        )


class TestSendingIntervalCheckerService:
    @pytest.mark.django_db
    def test_can_be_sent(self, email_verification: EmailVerification):
        email_verification.created_at -= EV_SENDING_INTERVAL_TIMEDELTA

        assert is_ev_sending_interval_passed(EVConverter().to_dto(email_verification))
        assert is_ev_sending_interval_passed(None)

    @pytest.mark.django_db
    def test_cannot_be_sent(
        self,
        email_verification: EmailVerification,
    ):
        assert not is_ev_sending_interval_passed(
            EVConverter().to_dto(email_verification)
        )


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
    user_schema = UserConverter().to_dto(
        mixer.blend("users.User", is_verified=is_verified)
    )
    email_verification_schema = (
        EVConverter().to_dto(mixer.blend("users.EmailVerification"))
        if previous_sending
        else None
    )

    availability_status = get_ev_sending_availability_status(
        user_schema, email_verification_schema
    )

    assert availability_status == expected_status


if __name__ == "__main__":
    pytest.main()
