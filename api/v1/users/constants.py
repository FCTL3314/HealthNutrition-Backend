from datetime import timedelta

USERS_PAGINATE_BY = 12

USERS_ORDERING = ("username",)

EV_SENDING_SECONDS_INTERVAL = 60
EV_EXPIRATION_SECONDS = 7200

EV_SENDING_INTERVAL_TIMEDELTA = timedelta(seconds=EV_SENDING_SECONDS_INTERVAL)
EV_EXPIRATION_TIMEDELTA = timedelta(seconds=EV_EXPIRATION_SECONDS)

EV_CODE_LENGTH = 8

ALLOWED_DJOSER_ENDPOINTS = (
    "users-me",
    "users-detail",
    "users-list",
    "users-set-password",
    "users-reset-password",
    "users-reset-password-confirm",
)
