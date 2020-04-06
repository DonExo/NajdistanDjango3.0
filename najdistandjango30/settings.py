import os

# .env file
from dotenv import load_dotenv
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMINS = [('Don', 'admin@gmail.com')]
AUTH_USER_MODEL = 'users.User'

SECRET_KEY = os.getenv('SECRET_KEY', 'very_secret_key')
DEBUG = os.getenv('DEBUG', False)
ALLOWED_HOSTS = ["*"]

# Needed for Debug Toolbar
INTERNAL_IPS = [ '127.0.0.1' ]

# # AWS Related / Enable this to allow upload to AWS
# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_LOCATION = 'static'
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
# STATIC_URL = 'https://{}/{}/'.format(AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# DEFAULT_FILE_STORAGE = 'listings.s3_backend.MediaStorage'

# Disable this if above is enabled
STATIC_URL = '/static/'

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
    'django.contrib.humanize',

    'django.contrib.sites',
    'registration',
    'django.contrib.admin',

    # Third party libraries
    'debug_toolbar',
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

    # Django debug toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',

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

WSGI_APPLICATION = 'najdistandjango30.wsgi.application'

ENV_DB_SQLITE_NAME = os.getenv("DB_SQLITE_NAME", 'najdistan.db')
ENV_DB_POSTGRE_NAME = os.getenv("DB_POSTGRE_NAME")
ENV_DB_USERNAME = os.getenv('DB_USERNAME')
ENV_DB_PASSWORD = os.getenv('DB_PASSWORD')
ENV_DB_HOST = os.getenv('DB_HOST')

if DEBUG: # If we are in Debug - means we are still developing, hence we are fine with an SQlite database
    sqlite_engine = 'django.db.backends.sqlite3',
    DATABASES = {
        'default': {
            'ENGINE': sqlite_engine,
            'NAME': os.path.join(BASE_DIR, ENV_DB_SQLITE_NAME),
        }
    }

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

else: # Otherwise we are using fully-fledged postgres database
    postgre_engine = 'django.db.backends.postgresql_psycopg2'
    DATABASES = {
        'default': {
            'ENGINE': postgre_engine,
            'NAME': ENV_DB_POSTGRE_NAME,
            'USER': ENV_DB_USERNAME,
            'PASSWORD': ENV_DB_PASSWORD,
            'HOST': ENV_DB_HOST,
            'PORT': '',
        }
    }

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True
