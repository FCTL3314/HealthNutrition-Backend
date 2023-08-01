from core.settings.base import *

# Security

DEBUG = False

INTERNAL_IPS = env.list("INTERNAL_IPS")

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASSWORD"),
        "HOST": env("DATABASE_HOST"),
        "PORT": env("DATABASE_PORT"),
    }
}

# Email

EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_PORT = env.str("EMAIL_PORT")
DEFAULT_FROM_EMAIL = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")
