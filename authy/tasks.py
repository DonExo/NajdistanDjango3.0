# from __future__ import absolute_import, unicode_literals
from celery import shared_task
from django.shortcuts import get_object_or_404

from users.models import User


@shared_task
def task_send_password_change_confirmation_email(user_pk):
    # It's not needed to gracefully handle errors here
    # For whatever reason the task fails, we want to see the stacktrace and error in Django Admin Task Results
    user = get_object_or_404(User, pk=user_pk)

    # TODO: Fix this with a proper HTML template (when the time comes)
    user.email_user("Password changed!",
                    f"Dear {user.first_name}. \n"
                    f"This is to inform you that your password has been successfully changed.")
    return f"Password change confirmation email successfully sent to {user.email}"

