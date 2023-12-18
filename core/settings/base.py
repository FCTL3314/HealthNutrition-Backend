from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Environment variables

env = environ.Env()

environ.Env.read_env(BASE_DIR / ".env")

# Security

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    "cacheops",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django_cleanup",
    "rest_framework",
    "rest_framework_simplejwt",
    "django_filters",
    "corsheaders",
    "drf_spectacular",
    "silk",
    "mptt",
    "django_summernote",
    "api",
    "api.v1",
    "api.v1.users",
    "api.v1.auth",
    "api.v1.categories",
    "api.v1.nutrition",
    "api.v1.products",
    "api.v1.diets",
    "api.v1.comparisons",
    "api.v1.comments",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Redis

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.str("REDIS_PORT")

REDIS_URI = f"redis://{REDIS_HOST}:{REDIS_PORT}"

# RabbitMQ

RABBITMQ_HOST = env.str("RABBITMQ_HOST")
RABBITMQ_PORT = env.str("RABBITMQ_PORT")

BASE_RABBITMQ_URI = f"://guest:guest@{RABBITMQ_HOST}:{RABBITMQ_PORT}"
RABBITMQ_AMQP_URI = f"amqp{BASE_RABBITMQ_URI}"
RABBITMQ_RPC_URI = f"rpc{BASE_RABBITMQ_URI}"

# Cache

CACHEOPS_ENABLED = env.bool("IS_CACHE_ENABLED", True)

CACHEOPS_REDIS = {
    "host": REDIS_HOST,
    "port": REDIS_PORT,
    "db": 1,
}

CACHEOPS = {
    "users.User": {
        "ops": "all",
        "timeout": 30 * 60,
    },
    "products.Product": {
        "ops": "all",
        "timeout": 60 * 60,
    },
    "categories.Category": {
        "ops": "all",
        "timeout": (60 * 60) * 2,
    },
    "comments.Comment": {
        "ops": "all",
        "timeout": 60 * 30,
    },
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files

STATIC_URL = "static/"

# Media files

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Frontend

FRONTEND_URL = env.str("FRONTEND_URL", default="http://localhost:5173")
FRONTEND_PASSWORD_RESET_CONFIRM_URL = env.str(
    "FRONTEND_PASSWORD_RESET_URL",
    default="users/auth/password-reset/confirm/{uid}/{token}/",
)

# Users

AUTH_USER_MODEL = "users.User"

LOGIN_URL = "/users/login/"
LOGOUT_REDIRECT_URL = "/"

# Email

EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")

# Celery

CELERY_BROKER_URL = RABBITMQ_AMQP_URI
CELERY_RESULT_BACKEND = RABBITMQ_RPC_URI

CELERY_TASK_TIME_LIMIT = 60 * 5

# Rest Framework

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

# Spectacular API documentation

SPECTACULAR_SETTINGS = {
    "TITLE": "Store Tracker API",
    "DESCRIPTION": (
        "Django / DRF based app for comparing prices between " "different stores."
    ),
    "CONTACT": {
        "email": "solovev.nikita.05@gmail.com",
    },
    "LICENSE": "Apache 2.0",
    "VERSION": "1.0.0",
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
    "SWAGGER_UI_SETTINGS": {
        "filter": True,
    },
    "SERVE_INCLUDE_SCHEMA": False,
}

# Simple JWT

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=120),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# Djoser

DJOSER = {
    "HIDE_USERS": False,
    "USER_ID_FIELD": "slug",
    "PERMISSIONS": {
        "current_user": ("rest_framework.permissions.IsAuthenticated",),
        "user": ("rest_framework.permissions.AllowAny",),
        "user_list": ("rest_framework.permissions.AllowAny",),
    },
    "SERIALIZERS": {
        "user": "api.v1.users.serializers.UserSerializer",
        "current_user": "api.v1.users.serializers.CurrentUserSerializer",
        "user_create": "api.v1.users.serializers.UserCreateSerializer",
    },
    "EMAIL": {
        "password_reset": "api.v1.users.email.PasswordResetEmail",
    },
    "PASSWORD_RESET_CONFIRM_URL": f"{FRONTEND_URL}/{FRONTEND_PASSWORD_RESET_CONFIRM_URL}",
}
