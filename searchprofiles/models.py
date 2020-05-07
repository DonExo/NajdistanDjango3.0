from django.db import models

from configdata import LISTING_TYPE_2, UPDATE_FREQUENCIES, INTERIOR_CHOICES
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from users.models import BaseModel, User
from .managers import CustomSearchProfileQueryset


class SearchProfiles(BaseModel):
    """
    A class used for saving user Search Profiles.
    Will be used for informing a user when a listings is in his listings criteria
    """
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name='searchprofiles')
    title = models.CharField(_("Name your Search Profile"), max_length=255, null=True)
    city = models.ForeignKey("listings.Place", on_delete=models.DO_NOTHING)
    listing_type = models.CharField(_('Listing type'), max_length=10, default='rent', choices=LISTING_TYPE_2,
                                    help_text=_('Designates the type of search profile: rent or sell'))
    rooms = models.PositiveSmallIntegerField(_("Number of rooms"), default=2)
    bedrooms = models.PositiveSmallIntegerField(_("Number of bedrooms"), default=1)
    min_price = models.DecimalField(_("Minimum price"), max_digits=9, decimal_places=0)
    max_price = models.DecimalField(_("Maximum price"),  max_digits=9, decimal_places=0)
    interior = models.CharField(max_length=15, choices=INTERIOR_CHOICES, default='unspecified')
    frequency = models.CharField(_("Update frequency"), choices=UPDATE_FREQUENCIES, default='weekly', max_length=255)
    is_active = models.BooleanField(default=True)

    objects = CustomSearchProfileQueryset.as_manager()

    class Meta:
        unique_together = ('user', 'title')
        verbose_name_plural = 'Search profiles'

    def __str__(self):
        return self.title

    def clean(self):
        if self.rooms < self.bedrooms:
            raise ValidationError({'rooms': "You can not have less rooms than bedrooms"})
        if self.min_price > self.max_price:
            raise ValidationError({'min_price': "Minimum price can't be bigger than maximum price"})

