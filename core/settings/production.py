from core.settings.base import *

# Security

DEBUG = False

# Static files

STATIC_ROOT = BASE_DIR / "static"

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

# Logging

MAX_LOG_FILE_SIZE = (1024 * 1024) * 10  # 10 MB

COMMON_FILE_HANDLER_KWARGS = {
    "class": "logging.handlers.RotatingFileHandler",
    "maxBytes": MAX_LOG_FILE_SIZE,
    "backupCount": 10,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime} | {levelname}] - {filename} on line {lineno}:\n{message}\n\n",
            "datefmt": "%Y/%b/%d %H:%M:%S",
            "style": "{",
        },
        "simple": {
            "format": "[{asctime} | {levelname}]:\n{message}\n\n",
            "datefmt": "%Y/%b/%d %H:%M:%S",
            "style": "{",
        },
    },
    "handlers": {
        "django_file": {
            **COMMON_FILE_HANDLER_KWARGS,
            "formatter": "verbose",
            "filename": (BASE_DIR / "logs/django.log"),
        },
        "mailing_file": {
            **COMMON_FILE_HANDLER_KWARGS,
            "formatter": "simple",
            "filename": (BASE_DIR / "logs/mailing.log"),
            "level": "INFO",
        },
        "accounts_file": {
            **COMMON_FILE_HANDLER_KWARGS,
            "formatter": "simple",
            "filename": (BASE_DIR / "logs/accounts.log"),
            "level": "INFO",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["django_file"],
            "level": "WARNING",
        },
        "mailings": {
            "handlers": ["mailing_file"],
            "level": "DEBUG",
        },
        "accounts": {
            "handlers": ["accounts_file"],
            "level": "DEBUG",
        },
    },
}
