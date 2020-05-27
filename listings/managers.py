from django.db import models
from django.db.models import Q


class CustomListingQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_approved=True, is_available=True)

    def inactive(self):
        return self.filter(is_approved=True, is_available=False)

    def pending(self):
        return self.filter(Q(is_approved=None) | Q(is_approved=False))

    def approved(self):
        return self.filter(is_approved=True)

    def rejected(self):
        return self.filter(is_approved=False)

    def delete(self):
        for object in self:
            object.delete()
