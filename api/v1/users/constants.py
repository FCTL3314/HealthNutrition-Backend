from datetime import timedelta

from core.settings.base import env

MAX_USER_IMAGE_SIZE_MB = 10

USERS_PAGINATE_BY = 12

USERS_ORDERING = ("username",)

EV_SENDING_INTERVAL = env.int("EV_SENDING_INTERVAL")
EV_SENDING_INTERVAL_TIMEDELTA = timedelta(seconds=EV_SENDING_INTERVAL)

EV_EXPIRATION = env.int("EV_EXPIRATION")
EV_EXPIRATION_TIMEDELTA = timedelta(seconds=EV_EXPIRATION)

EV_CODE_LENGTH = 8

ALLOWED_DJOSER_ENDPOINTS = (
    "users-me",
    "users-detail",
    "users-list",
    "users-set-password",
    "users-reset-password",
    "users-reset-password-confirm",
)
