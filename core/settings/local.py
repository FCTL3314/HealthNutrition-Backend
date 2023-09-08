from core.settings.base import *

# Static files

STATICFILES_DIRS = (BASE_DIR / "static",)

# Email

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
