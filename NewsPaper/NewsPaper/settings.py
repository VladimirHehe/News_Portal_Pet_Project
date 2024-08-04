import os
from pathlib import Path
from .config import pass_to_email, Broker_Redis
import socket

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vj_d1tp8w(2z^7_t1xfknwg0&d(h+46$jq6t0gmlmj+ds!!uyl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SERVER_NAME = 'localhost'

# Application definition

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news.apps.NewsConfig',
    'accounts',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'django_apscheduler',
    'NewsPaper',


]
APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25  # Seconds

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.locale.LocaleMiddleware',

]

ROOT_URLCONF = 'NewsPaper.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'NewsPaper.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru'
LANGUAGES = [
    ('ru', 'Русский'),
    ('en', 'English'),
]

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ACCOUNT_FORMS = {'signup': 'news.forms.CommonSignupForm'}

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

LOGIN_URL = '/accounts/login/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

ACCOUNT_CONFIRM_EMAIL_ON_GET = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_SSL = True

EMAIL_HOST_USER = 'sobetskyvladimir@yandex.ru'
EMAIL_HOST_PASSWORD = pass_to_email

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
EMAIL_ADMIN = EMAIL_HOST_USER

CELERY_BROKER_URL = Broker_Redis
CELERY_RESULT_BACKEND = Broker_Redis
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },

    'formatters': {
        'console': {
            'format': '%(asctime)s %(levelname)s %(message)s',
        },
        'console_warning': {
            'format': "%(asctime)s %(levelname)s %(pathname)s %(message)s",
        },
        'console_error': {
            'format': "%(asctime)s %(levelname)s %(pathname)s %(exc_info)s %(message)s",
        },
        'console_critical': {
            'format': "%(asctime)s %(levelname)s %(pathname)s %(exc_info)s %(message)s",
        },
        'general': {
            'format': "%(asctime)s %(levelname)s %(module)s %(message)s",
        },
        'errors': {
            'format': "%(asctime)s %(levelname)s %(pathname)s %(exc_info)s %(message)s",
        },
        'errors_critical': {
            'format': "%(asctime)s %(levelname)s %(pathname)s %(exc_info)s %(message)s",
        },
        'security': {
            'format': "%(asctime)s %(levelname)s %(module)s %(message)s",
        },
        'mail': {
            'format': "%(asctime)s %(levelname)s %(pathname)s %(message)s",
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'formatter': 'console',
        },
        'console_warning': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'filters': ['require_debug_true'],
            'formatter': 'console_warning',
        },
        'console_error': {
            'class': 'logging.StreamHandler',
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'formatter': 'console_error',
        },
        'console_critical': {
            'class': 'logging.StreamHandler',
            'level': 'CRITICAL',
            'filters': ['require_debug_true'],
            'formatter': 'console_critical',
        },
        'general': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'formatter': 'general',
            'filename': os.path.join(BASE_DIR, 'loggers', 'general.log')
        },
        'errors': {
            'class': 'logging.FileHandler',
            'level': 'ERROR',
            'formatter': 'errors',
            'filename': os.path.join(BASE_DIR, 'loggers', 'errors.log'),
        },
        'errors_critical': {
            'class': 'logging.FileHandler',
            'level': 'CRITICAL',
            'formatter': 'errors_critical',
            'filename': os.path.join(BASE_DIR, 'loggers', 'errors.log'),
        },
        'security': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'security',
            'filename': os.path.join(BASE_DIR, 'loggers', 'security.log'),
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter': 'mail',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console', 'general', 'console_warning', 'console_critical', 'console_error', ],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['mail_admins', 'errors', 'errors_critical', ],
            'level': 'ERROR',
        },
        'django.server': {
            'handlers': ['errors', 'errors_critical', 'mail_admins', ],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['errors'],
            'level': 'ERROR',
        },
        'django.db.backends': {
            'handlers': ['errors'],
            'level': 'ERROR',
        },
        'django.security': {
            'handlers': ['security', ],
            'level': 'INFO',
        },
    },
}
