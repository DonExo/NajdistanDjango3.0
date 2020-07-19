from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta
from celery import shared_task

from listings.models import Listing
from searchprofiles.models import SearchProfiles


def get_time_offset(value):
    """

    :param value: ... ?
    :return: A datetime object?
    """
    now = datetime.now()
    if value == 'daily':
        offset = now - timedelta(days=1)
    elif value == 'weekly':
        offset = now - timedelta(weeks=1)
    elif value == 'biweekly':
        offset = now - timedelta(weeks=2)
    elif value == 'monthly':
        offset = now - timedelta(days=30)
    else:
        print("Invalid choice!")
        offset = None
    return offset

@shared_task
def send_info_to_user(sp_pk: int, listings_pk: int) -> int:
    # Make this a real INFO e-mail for the user
    sp = SearchProfiles.objects.get(pk=sp_pk)
    sp.user.email_user("SP Subject", f"A total of {len(listings_pk)} have been found for your SP {sp.title}")
    print(f"Active: [[{sp.title}]] - Sending info to {sp.user.email} with {len(listings_pk)} new listings")

    return 1

@shared_task
def get_new_listings(offset_value: str) -> int:
    """
    A celery task that informs the users with active Search Profiles and matching criteria of newly posted listings.

    The task is used in combination with django-celery-beat.
    There are 4 pre-defined Periodic Tasks in the DB.
    The values are: daily, weekly, biweekly and monthly.
    NOTE: The 'instant' option of the Search Profiles are handled in a separate celery task.


    :param offset_value: An offset value (string) that can be any of: instant, daily, weekly, biweekly and monthly
    :return: ...
    """

    # Chaining?

    print(f"Received offset value: '{offset_value}'")
    search_profiles = SearchProfiles.objects.active(frequency=offset_value)
    if not search_profiles.exists():
        print(f"No active Search Profiles with '{offset_value}' value. EXITING")
        return -1
    print(f"Found {search_profiles.count()} search profile(s) for the given offset value.")

    # calculate the offset value depending on the string
    offset_period = get_time_offset(offset_value)

    # TODO: This should rather be "approved_at__gte", but that field does not exists in the model yet
    # TODO: Make this a real Search profile with all relevant data
    # TODO: Exclude their own Listings (if any)

    matching_listings_pks = Listing.objects.active(created_at__gte=offset_period).values_list('pk', flat=True)
    # print(f"Found {len(matching_listings_pks)} listings!")

    for search_profile in search_profiles:
        send_info_to_user.delay(search_profile.pk, list(matching_listings_pks))
        # JSON-only serializable data, no model objects or QuerySets

