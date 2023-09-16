from core.settings.base import *

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Cache

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

# Email

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"
