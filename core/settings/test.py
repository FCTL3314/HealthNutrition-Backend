from core.settings.base import *

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Cache

CACHEOPS_REDIS["db"] = 2

# Email

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
