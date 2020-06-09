from __future__ import absolute_import, unicode_literals

from datetime import datetime, timedelta
from celery import shared_task

from listings.models import Listing
from searchprofiles.models import SearchProfiles


def get_time_offset(value):
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
def send_info_to_user(sp_pk, listings_pk):
    # Make this a real INFO e-mail for the user
    sp = SearchProfiles.objects.get(pk=sp_pk)
    sp.user.email_user("SP Subject", f"A total of {len(listings_pk)} have been found for your SP {sp.title}")
    print(f"Active: [[{sp.title}]] - Sending info to {sp.user.email} with {len(listings_pk)} new listings")

@shared_task
def get_new_listings(value):
    # Add some debugging eventually?
    print(f"Receiving value '{value}'")
    search_profiles = SearchProfiles.objects.filter(frequency=value, is_active=True)
    if not search_profiles.exists():
        print(f"No active '{value}' Search Profiles with. EXITING")
        return

    offset = get_time_offset(value)

    # TODO: This should rather be "approved_at__gte", but that field does not exists in the model yet
    # TODO: Make this a real Search profile with all relevant data
    # TODO: Exclude their own Listings (if any)
    matching_listings_pks = Listing.objects.filter(created_at__gte=offset).values_list('pk', flat=True)
    print(f"Found {len(matching_listings_pks)} listings!")

    for search_profile in search_profiles:
        send_info_to_user.delay(search_profile.pk, list(matching_listings_pks))
        # JSON-only serializable data, no model objects or QuerySets

