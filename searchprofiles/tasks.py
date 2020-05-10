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
    sp = SearchProfiles.objects.get(pk=sp_pk)
    sp.user.email_user("SP Subject", f"A total of {len(listings_pk)} have been found for your SP {sp.title}")
    print(f"Active: [[{sp.title}]] - Sending info to {sp.user.email} with {len(listings_pk)} new listings")

@shared_task
def get_new_listings(value): # i.e. 'daily', 'weekly'
    print(f"Receiving value '{value}'")
    sps = SearchProfiles.objects.filter(frequency=value, is_active=True)
    if not sps.exists():
        print(f"No active users with '{value}' SP. EXITING")
        return

    offset = get_time_offset(value)

    # TODO: This should rather be "approved_at__gte", but that field does not exists in the model yet
    listings_pk = Listing.objects.filter(created_at__gte=offset).values_list('pk', flat=True)
    print(f"Found {len(listings_pk)} listings!")

    for sp in sps:
        send_info_to_user.delay(sp.pk, list(listings_pk))
