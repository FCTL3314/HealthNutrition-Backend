import socket
from core.settings.base import *

# Security

# Way to have debug toolbar when developing with docker
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

# Application definition

INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = (BASE_DIR / "frontend/static",)

# Email

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
