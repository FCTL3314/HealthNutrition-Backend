from pathlib import Path

import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Environment variables

env = environ.Env()

environ.Env.read_env(BASE_DIR / '.env')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INTERNAL_IPS = env.list('INTERNAL_IPS')

DOMAIN_NAME = env.str('DOMAIN_NAME')

PROTOCOL = env.str('PROTOCOL')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'widget_tweaks',

    'users',
    'stores',
    'products',
    'comparisons',
    'interactions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')

    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['frontend/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'common.context_processors.current_url_name',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Redis

REDIS_HOST = env.str('REDIS_HOST')
REDIS_PORT = env.str('REDIS_PORT')

# Cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}',
        'OPTIONS': {
            'db': '1',
        }
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
if DEBUG:
    STATICFILES_DIRS = (BASE_DIR / 'frontend/static',)
else:
    STATIC_ROOT = BASE_DIR / 'frontend/static'

# Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}'

CELERY_TASK_TIME_LIMIT = 60 * 30

# Users

AUTH_USER_MODEL = 'users.User'

LOGOUT_REDIRECT_URL = '/'

USER_VIEW_TRACKING_CACHE_TIME = (60 * 60) * 12

# Products

PRICE_ROUNDING = 2

PRODUCTS_PAGINATE_BY = 12

POPULAR_PRODUCT_TYPES_CACHE_KEY = 'popular_product_types'
PRODUCTS_CACHE_KEY = 'products_product_type:{id:}'
PRODUCT_TYPE_VIEW_TRACKING_CACHE_KEY = 'address:{addr:}_product_type:{id:}'
PRODUCT_VIEW_TRACKING_CACHE_KEY = 'address:{addr:}_product:{id:}'

POPULAR_PRODUCT_TYPES_CACHE_TIME = 60 * 60
PRODUCTS_CACHE_TIME = 60 * 60

# Stores

STORE_VIEW_TRACKING_CACHE_KEY = 'address:{addr:}_store:{id:}'

STORE_VIEW_TRACKING_CACHE_TIME = 60 * 30

# Interactions

COMMENTS_PAGINATE_BY = 3

# Email

EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_HOST = env.str('EMAIL_HOST')
    EMAIL_PORT = env.str('EMAIL_PORT')
    DEFAULT_FROM_EMAIL = env.str('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
    EMAIL_USE_SSL = env.bool('EMAIL_USE_SSL')

EMAIL_SEND_INTERVAL_SECONDS = 60
EMAIL_EXPIRATION_HOURS = 3600 * 2
