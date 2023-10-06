from core.settings.base import *

# Security

DEBUG = True

# Application definition

MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")

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

# Static files

STATICFILES_DIRS = (BASE_DIR / "static",)

# Email

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
