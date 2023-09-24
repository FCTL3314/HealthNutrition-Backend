from core.settings.base import *

# Security

DEBUG = True

# Application definition

MIDDLEWARE.insert(0, "silk.middleware.SilkyMiddleware")

# Static files

STATICFILES_DIRS = (BASE_DIR / "static",)

# Email

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
