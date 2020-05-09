from __future__ import absolute_import, unicode_literals

import os
# from django.conf import settings
from celery import Celery

# if settings.DEBUG:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'najdistandjango30.settings.local')
# else:
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'najdistandjango30.settings.production')


app = Celery('najdistandjango30')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()



##################
# Make sure you have rabbitmq (or other broker) up and running
# sudo rabbitmq-server

# Make sure to have the celery worker up and running
# celery -A najdistandjango30 worker --loglevel=info