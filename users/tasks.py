from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404

from datetime import datetime, timedelta
from celery import shared_task

from listings.models import Listing
from users.models import User
from searchprofiles.models import SearchProfiles


@shared_task
def send_info_to_user(sp_pk, listings_pk):
    # Make this a real INFO e-mail for the user
    sp = SearchProfiles.objects.get(pk=sp_pk)
    sp.user.email_user("SP Subject", f"A total of {len(listings_pk)} have been found for your SP {sp.title}")
    print(f"Active: [[{sp.title}]] - Sending info to {sp.user.email} with {len(listings_pk)} new listings")


# TODO: Make good template for this
@shared_task
def send_deactivation_email(user_pk):
    user = get_object_or_404(User, pk=user_pk)
    print(f"in celery task: {user}")
    user.email_user("Account deactivated",
                    "Hi {}. <br/> This is a confirmation e-mail to let you know that your "
                    "account has been successfuly deactivated".format(user.first_name),
                    )
