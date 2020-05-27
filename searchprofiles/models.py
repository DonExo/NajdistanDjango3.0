from django.db import models

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
    title = models.CharField(max_length=255, null=True)
    city = models.ForeignKey("listings.Place", on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(default=True)

    # Number fields
    rooms = models.PositiveSmallIntegerField(_("Number of rooms"), null=True, blank=True)
    bedrooms = models.PositiveSmallIntegerField(_("Number of bedrooms"), null=True, blank=True)
    min_price = models.DecimalField(_("Minimum price"), max_digits=9, decimal_places=0)
    max_price = models.DecimalField(_("Maximum price"),  max_digits=9, decimal_places=0)

    # Choices fields
    home_type = models.CharField(_('Home type'), max_length=50, null=True, blank=True)
    listing_type = models.CharField(_('Listing type'), max_length=5, null=True, blank=True)
    interior = models.CharField(_('Interior'), max_length=50, null=True, blank=True)
    frequency = models.CharField(_("Update frequency"), max_length=50)

    objects = CustomSearchProfileQueryset.as_manager()

    class Meta:
        unique_together = ('user', 'title')
        verbose_name_plural = 'Search profiles'

    def __str__(self):
        return self.title

    def clean(self):
        if self.rooms and self.bedrooms and self.rooms < self.bedrooms:
            raise ValidationError({'rooms': "You can not have less rooms than bedrooms"})
        if self.min_price and self.max_price and self.min_price > self.max_price:
            raise ValidationError({'min_price': "Minimum price can't be bigger than maximum price"})

