from django.db import models


class CustomListingQuerySet(models.QuerySet):
    def approved(self):
        return self.filter(is_approved=True)

    def rejected(self):
        return self.filter(is_approved=False)

    def delete(self):
        for object in self:
            object.delete()
