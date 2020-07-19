from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404

from celery import shared_task

from users.models import User


# TODO: Make good template for this
@shared_task
def send_deactivation_email(user_pk):
    user = get_object_or_404(User, pk=user_pk)
    user.email_user("Account deactivated",
                    "Hi {}. This is a confirmation e-mail to let you know that your "
                    "account has been successfuly deactivated".format(user.first_name),
                    )
