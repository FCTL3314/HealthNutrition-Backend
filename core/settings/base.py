from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environment variables

env = environ.Env()

environ.Env.read_env(BASE_DIR / '.env')

SECRET_KEY = env.str('SECRET_KEY')

# Security

DEBUG = True

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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend/templates'],
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

# Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Users

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = '/users/login/'
LOGOUT_REDIRECT_URL = '/'

VISITS_CACHE_TIME = (60 * 60) * 12

# Products

PRICE_ROUNDING = 2

PRODUCTS_PAGINATE_BY = 24
PRODUCT_TYPES_PAGINATE_BY = 12

PRODUCT_TYPES_CACHE_KEY = 'popular_product_types'
PRODUCTS_CACHE_TEMPLATE = 'products_product_type:{product_id:}'

PRODUCT_TYPES_CACHE_TIME = 60 * 60
PRODUCTS_CACHE_TIME = 60 * 60

PRODUCTS_ORDERING = ('store__name', 'price')
PRODUCT_TYPES_ORDERING = ('-product__store__count', '-views')

PRODUCT_TYPE_VIEW_TRACKING_CACHE_TEMPLATE = 'address:{addr:}_product_type:{id:}'
PRODUCT_VIEW_TRACKING_CACHE_TEMPLATE = 'address:{addr:}_product:{id:}'

# Stores

STORE_VIEW_TRACKING_CACHE_KEY = 'address:{addr:}_store:{id:}'

STORE_VIEW_TRACKING_CACHE_TIME = 60 * 30

# Interactions

COMMENTS_PAGINATE_BY = 3

# Email

EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')

EMAIL_SEND_INTERVAL_SECONDS = 60
EMAIL_EXPIRATION_HOURS = (60 * 60) * 2

# Celery

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}'

CELERY_TASK_TIME_LIMIT = 60 * 5
