import os

from dotenv import load_dotenv
from pathlib import Path  # python3 only
from datetime import timedelta
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

BASE_DIR = os.path.dirname(os.path.dirname((os.path.dirname(os.path.abspath(__file__)))))

ADMINS = [('Don', 'admin@gmail.com')]
AUTH_USER_MODEL = 'users.User'

SECRET_KEY = os.getenv('SECRET_KEY', 'very_secret_key')

ALLOWED_HOSTS = [""]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Django-registration-redux
ACCOUNT_ACTIVATION_DAYS = 1
SITE_ID = 1

LOGIN_REDIRECT_URL = '/'

INSTALLED_APPS = [
    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',

    'django.contrib.humanize',

    'django.contrib.sites',
    'registration', # django-registration-redux, needs to be at this position
    'django.contrib.admin',

    # Third party libraries
    'storages',

    # Local apps
    'users',
    'listings',
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
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAdminUser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # enable this if you want session auth
        # 'rest_framework.authentication.BasicAuthentication',  # enable this if you want to auth with user+pass
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # enable this if you need Browsable API
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),  # Token expiration
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # Refresh token expiration
}

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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
