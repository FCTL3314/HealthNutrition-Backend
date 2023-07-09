import socket
from core.settings.base import *

# Security

# Way to have debug toolbar when developing with docker
ip = socket.gethostbyname(socket.gethostname())

INTERNAL_IPS += (ip[:-1] + "1",)

# Application definition

INSTALLED_APPS.append("debug_toolbar")

MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = (BASE_DIR / "frontend/static",)

# Email

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
