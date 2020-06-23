import os

from django.urls import reverse_lazy
from dotenv import load_dotenv
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

BASE_DIR = os.path.dirname(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))

ADMINS = [('Admin', )]
MANAGERS = ADMINS
AUTH_USER_MODEL = 'users.User'

SECRET_KEY = os.getenv('SECRET_KEY', 'very_secret_key')

ALLOWED_HOSTS = [""]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Django-registration-redux
ACCOUNT_ACTIVATION_DAYS = 1
SITE_ID = 1

LOGIN_URL = reverse_lazy('authy:login')
LOGIN_REDIRECT_URL = reverse_lazy('accounts:profile')
LOGOUT_REDIRECT_URL = reverse_lazy('index')

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Google ReCaptcha keys (and their TEST keys as default values)
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY', '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe')
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# Required by django-registration-redux
INCLUDE_REGISTER_URL = False
INCLUDE_AUTH_URLS = False
# REGISTRATION_OPEN = False  # Disables registering of new users

GENERATE_DUMMY_LISTING = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CELERY related settings
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379')
# CELERY_RESULT_BACKEND = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = 'django-db'  # django-celery-results
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

# This is the main setting for triggering Celery. It is inherited in the local.py and production.py settings
# CELERY_TASK_ALWAYS_EAGER = True

# https://docs.celeryproject.org/en/stable/django/first-steps-with-django.html#extensions

INSTALLED_APPS = [
    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',
    'registration',  # django-registration-redux, needs to be at this position
    'django.contrib.admin',

    # Third party libraries
    'storages',
    'django_filters',
    'captcha',
    'widget_tweaks',
    # Celery libraries
    'django_celery_results',
    'django_celery_beat',

    # Local apps
    'authy',
    'users',
    'listings',
    'searchprofiles',
    'reports',
    'api',
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

ROOT_URLCONF = 'najdistandjango30.urls'

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
                'users.context_processors.add_project_name'
            ],
        },
    },
]

WSGI_APPLICATION = 'najdistandjango30.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Amsterdam'

USE_I18N = True

USE_L10N = True

USE_TZ = True
