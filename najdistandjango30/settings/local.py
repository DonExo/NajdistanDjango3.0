from .base import *

import os

DEBUG = True
ALLOWED_HOSTS = ["*"]

# Needed for Debug Toolbar
INTERNAL_IPS = [ '127.0.0.1' ]

STATIC_URL = '/static/'

INSTALLED_APPS += [
    'debug_toolbar',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    # Django debug toolbar (Needs to be at this position)
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'najdistan.db'),
    }
}

# Don't use Celery in local env. Change this to False if you explicitely want to use Celery locally
CELERY_TASK_ALWAYS_EAGER = True
