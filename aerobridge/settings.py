"""
Django settings for aerobridge project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import django_heroku
from pathlib import Path
import os

import moneyed
import sys
from os import environ as env
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.get('DJANGO_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'registry',
    'gcs_operations',
    'digitalsky_provider',
    'jetway',
    'launchpad',
    'pki_framework',
    'supply_chain_operations',
    'crispy_forms',
    "crispy_bootstrap5",
    "simple_history"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
]

ROOT_URLCONF = 'aerobridge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'jetway', 'templates'), os.path.join(BASE_DIR, 'launchpad', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'aerobridge.wsgi.application'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'aerobridge.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

SECURE_API_ENDPOINTS = False

# if DEBUG:
#     BROKER_URL = os.getenv("REDIS_URL",'redis://localhost:6379/')
# else:
#     BROKER_URL = os.getenv("REDIS_URL","redis://redis:6379/")
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'

# CELERY_RESULT_BACKEND = BROKER_URL

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'jetway.pagination.StandardResultsSetPagination',
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DATETIME_FORMAT': "%d-%b-%Y %H:%M:%S",
    'DEFAULT_AUTHENTICATION_CLASSES': (             
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        # 'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
    )
}


JWT_AUTH = {
    'JWT_PAYLOAD_GET_USERNAME_HANDLER':
        'pki_framework.utils.jwt_get_username_from_payload_handler',
    'JWT_DECODE_HANDLER':
        'pki_framework.utils.jwt_decode_token',
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': env.get("PASSPORT_AUDIENCE"),
    'JWT_ISSUER': env.get("PASSPORT_DOMAIN"),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SIMPLE_HISTORY_REVERT_DISABLED = True

CRYPTOGRAPHY_SALT = env.get(
    "CRYPTOGRAPHY_SALT", "__SET_AS_A_VERY_STRONG_PASSWORD__")
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

# Directory path to look for data fixture to load data into database before running tests
FIXTURE_DIRS = [os.getcwd() + '/tests/fixtures/']


# Currencies available for use
CURRENCIES = env.get(
    'ALLOWED_CURRENCY',
    [
        'AUD', 'CAD', 'EUR', 'GBP', 'JPY', 'NZD', 'USD','INR',
    ],
)

# Check that each provided currency is supported
for currency in CURRENCIES:
    if currency not in moneyed.CURRENCIES:  # pragma: no cover
        print(f"Currency code '{currency}' is not supported")
        sys.exit(1)
        
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
    }, 'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        }, 'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },

    }, 
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}



django_heroku.settings(locals())
