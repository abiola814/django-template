

import os
from datetime import timedelta
from .base import *


# SECRET_KEY='_g(cj$h(_i(%=j!jyjrq#4n2#_rd@*kvb_%h$_2b3-j^hg-wua'
# CORS


CORS_ALLOW_ALL_ORIGINS = True
# CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

SECRET_KEY=env("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
#     }
# }
# password validator


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
    "AUTH_HEADER_TYPES": ("Bearer","Token"),
    'UPDATE_LAST_LOGIN': True,
    "SIGNING_KEY": env('SECRET_KEY'),

}

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER='json'
CELERY_TASK_SERIALIZER='json'
CELERY_TIMEZONE = 'Africa/Lagos'

#store in db
CELERY_RESULT_BACKEND ='django-db'

# celery schedule

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

