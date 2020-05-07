from django.db import models


class CustomSearchProfileQueryset(models.QuerySet):
    def daily(self):
        return self.filter(frequency='daily', is_active=True)

    def weekly(self):
        return self.filter(frequency='weekly', is_active=True)

    def biweekly(self):
        return self.filter(frequency='biweekly', is_active=True)

    def monthly(self):
        return self.filter(frequency='monthly', is_active=True)
