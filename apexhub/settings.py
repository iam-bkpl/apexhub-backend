"""
Django settings for apexhub project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta

# from celery.schedules import crontab_parser

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-)wywzecw&u76hp!@#$#xse6i+d*-se&$%arar3+eprk1c*lhz%"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['apexhub.vercel.app' ,'apexhub-backend.vercel.app','*.vercel.app','bsatya.com.np','127.0.0.1',]

ALLOWED_HOSTS = []
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "drf_spectacular",
    "django_filters",
    "corsheaders",
    "rest_framework",
    "djoser",
    "rest_framework_swagger",
    "acs",
    "ashop",
    "core",
    "django_extensions",
    "drf_yasg",
    "ckeditor",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "apexhub.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # "DIRS": [],
        "DIRS": [os.path.join(BASE_DIR, "dist")],
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

WSGI_APPLICATION = "apexhub.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Database engine
        "NAME": BASE_DIR / "db.sqlite3",  # Database name
        "OPTIONS": {
            "timeout": 30,  # Connection timeout value (in seconds)
        },
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.mysql",
#         "NAME": "apexhub",
#         "USER": "root",
#         "PASSWORD": "lipak@123",
#         "HOST": "localhost",
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

# STATICFILES_DIRS = [os.path.join(BASE_DIR, "dist/static")]
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "core.CustomUser"


# REST_FRAMEWORK = {
#     # Use Django's standard `django.contrib.auth` permissions,
#     # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#     ]
# }

# DATETIME_FORMAT = 'Y-m-d\TH:i:s.u\Z'
REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ],
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    # "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    # "DEFAULT_SCHEMA_CLASS": "drf_yasg.openapi.SwaggerAutoSchema",
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
}

DJOSER = {
    "LOGIN_FIELD": "email",
    # "USER_CREATE_PASSWORD_RETYPE": True,
    # "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
    # "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
    # "SEND_CONFIRMATION_EMAIL": True,
    # "SET_USERNAME_RETYPE": True,
    # "SET_PASSWORD_RETYPE": True,
    "PASSWORD_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
    # "PASSWORD_RESET_CONFIRM_URL": "/http://localhost:5173/password/reset/confirm/{uid}/{token}",
    # "USERNAME_RESET_CONFIRM_URL": "email/reset/confirm/{uid}/{token}",
    # "ACTIVATION_URL": "activate/{uid}/{token}",
    # "SEND_ACTIVATION_EMAIL": True,
    # "SERIALIZERS": {
    #     "user_create": "core.serializers.UserCreateSerializer",
    #     "current_user": "core.serializers.UserSerializer",
    #     # "user": "core.serializers.CustomUserSerializer",
    # },
    "SERIALIZERS": {
        "user_create": "core.serializers.UserCreateSerializer",
        "user": "core.serializers.CustomUserSerializer",
        "current_user": "core.serializers.UserCreateSerializer",
        "user_delete": "djoser.serializers.UserDeleteSerializer",
    },
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
]
CORS_ORIGIN_WHITELIST = [
    "http://localhost:5173",
    "http://localhost:3000",
]
# CORS_ALLOW_ALL_ORIGINS = []

GRAPH_MODELS = {
    "all_applications": True,
    "graph_models": True,
}
SPECTACULAR_SETTINGS = {
    "TITLE": "Apex hub",
    "DESCRIPTION": "Apexshop and Apex CS",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # 'SERVE_INCLUDE_SCHEMA': True,
    "LOGIN_URL": "rest_framework:login"
    # OTHER SETTINGS
}

SWAGGER_SETTINGS = {
    "VALIDATOR_URL": "http://localhost:8189",
}

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "localhost"
# EMAIL_HOST_USER = "i.am.bhandari.kapil@gmail.com"
# EMAIL_HOST_PASSWORD = "cnjckcwblkehckzy"
# EMAIL_PORT = 25
# DEFAULT_FROM_EMAIL = "i.am.bhandari.kapil@gmail.com"
# ADMINS = "admin@admin.com"

EMAIL_HOST = "sandbox.smtp.mailtrap.io"
EMAIL_HOST_USER = "1022081c335d16"
EMAIL_HOST_PASSWORD = "c9c30ce4b483e0"
EMAIL_PORT = "2525"


CELERY_BROKER_URL = "redis://localhost:6379/1"
CELERY_BEAT_SCHEDULE = {
    "notify_students": {
        "task": "core.tasks.notify_students",
        # "schedule": crontab_parser(min_=1),
        "schedule": 5,
    }
}


# django debug
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
FRONTEND_BASE_URL = "http://localhost:5173"


CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = "https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": 900,
    },
}
