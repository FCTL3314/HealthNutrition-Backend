from django.conf import settings

VISITS_CACHE_TIME = (60 * 60) * 12

EV_SENDING_INTERVAL = settings.env.int("EV_SENDING_INTERVAL")
EV_EXPIRATION = settings.env.int("EV_EXPIRATION")

ALLOWED_DJOSER_ENDPOINTS = (
    "users-me",
    "users-detail",
    "users-list",
    "users-set-password",
    "users-reset-password",
    "users-reset-password-confirm",
)
