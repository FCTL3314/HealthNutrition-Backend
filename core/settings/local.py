from core.settings.base import *

# Security

DEBUG = True

# Static files

STATICFILES_DIRS = (BASE_DIR / "static",)

# Email

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
