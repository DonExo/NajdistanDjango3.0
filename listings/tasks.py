from __future__ import absolute_import, unicode_literals

from celery import shared_task

from users.models import User
from .models import Listing


@shared_task
def task_increment_visited_times_counter(listing_pk: int, user_pk: int) -> int:
    """
    Celery task for incrementing the 'times_visited' counter when visiting a property page
    Currently there is only one check: If the 'visiting' user is the owner of the property - do not increase it
    Otherwise, increase it always by one.
    @ TODO: In future iteration, introduce session management for only one increase per user session/ip

    :param listing_pk: A primary key (identifier) of the property
    :param user_pk: A primary key (identifier) of the visiting user, if any
    :return: Returns a success/error code from celery action
    """
    try:
        listing = Listing.objects.get(pk=listing_pk)
    except Listing.DoesNotExist:
        print("Listing not found")
        return -1

    try:
        user = User.objects.get(pk=user_pk)
    except User.DoesNotExist:
        user = None

    if user and user == listing.user:
        return -1

    listing.times_visited += 1
    listing.save()
    return 1