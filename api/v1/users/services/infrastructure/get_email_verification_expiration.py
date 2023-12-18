from datetime import datetime

from django.utils.timezone import now

from api.v1.users.constants import EV_EXPIRATION_TIMEDELTA


def get_email_verification_expiration() -> datetime:
    return now() + EV_EXPIRATION_TIMEDELTA
