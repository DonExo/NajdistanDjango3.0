from __future__ import absolute_import, unicode_literals

from celery import shared_task
from listings.models import Listing


@shared_task
def add(x, y):
    print(x+y)
    return x + y

@shared_task
def xx():
    import random
    deli = random.randint(0, 1)
    deli2 = random.randint(50, 100)
    return deli2 / deli
