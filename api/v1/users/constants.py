from core.settings.base import env

VISITS_CACHE_TIME = (60 * 60) * 12

EV_SENDING_INTERVAL = env.int("EV_SENDING_INTERVAL")
EV_EXPIRATION = env.int("EV_EXPIRATION")
EV_CODE_LENGTH = 8

ALLOWED_DJOSER_ENDPOINTS = (
    "users-me",
    "users-detail",
    "users-list",
    "users-set-password",
    "users-reset-password",
    "users-reset-password-confirm",
)
