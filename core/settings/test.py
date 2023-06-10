from core.settings.base import *

# Cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Email

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
