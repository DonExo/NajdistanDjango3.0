import os

# .env file
from dotenv import load_dotenv
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

ADMINS = [('Don', 'admin@gmail.com')]
AUTH_USER_MODEL = 'users.User'


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

ENV_SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = ENV_SECRET_KEY

ENV_DEBUG = os.getenv('DEBUG', False)
DEBUG = ENV_DEBUG

ALLOWED_HOSTS = ["*"]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Application definition

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party libraries


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
        'DIRS': [],
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# ENV_STATIC_URL = os.getenv('STATIC_URL', "'/static/'")
STATIC_URL = '/static/'
