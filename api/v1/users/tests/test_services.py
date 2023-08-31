from datetime import timedelta

import pytest

from api.common.time_providers import AbstractTimeProvider
from api.v1.users.constants import EV_SENDING_INTERVAL_TIMEDELTA
from api.v1.users.models import EmailVerification
from api.v1.users.services.data_transfer import EVAdapter
from api.v1.users.services.email_verification import EVNextSendingTimeService


@pytest.mark.django_db
def test_next_sending_time_calculator(
    email_verification: EmailVerification,
    utc_time_provider: AbstractTimeProvider,
):
    email_verification.created_at = (
        utc_time_provider.now - EV_SENDING_INTERVAL_TIMEDELTA
    )
    next_sending_datetime = EVNextSendingTimeService(
        EVAdapter().to_dto(email_verification)
    ).execute()
    assert next_sending_datetime == pytest.approx(
        utc_time_provider.now, abs=timedelta(seconds=1)
    )


if __name__ == "__main__":
    pytest.main()
