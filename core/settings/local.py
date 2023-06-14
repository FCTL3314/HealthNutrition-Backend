from core.settings.base import *

# Application definition

INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = (BASE_DIR / "frontend/static",)

# Email

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
