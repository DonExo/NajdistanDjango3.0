from __future__ import absolute_import, unicode_literals

from celery import shared_task
from listings.models import Listing


@shared_task
def add(x, y):
    print(x+y)
    return x + y

@shared_task
def minus(x, y):
    print(x-y)
    return x - y

@shared_task
def mnozi(x, y):
    print(x*y)
    return x * y

@shared_task
def something():
    print(mnozi(2, 3) + 4)

@shared_task
def xx(pk):
    obj = Listing.objects.get(pk=pk)
    print(obj.pk)
    import random
    obj.title = f"Zelka melka: {random.random()}"
    obj.save()