from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

from users.models import BaseModel, User
from configdata import REGEX_ZIPCODE_VALIDATOR, HOME_TYPE, INTERIOR_CHOICES, \
    LISTING_TYPE, LISTING_TYPE_2, UPDATE_FREQUENCIES


class Place(models.Model):
    """
    A class that represents a place/region
    """
    region = models.CharField(_('Region'), max_length=255)
    city = models.CharField(_('City'), max_length=255)

    def __str__(self):
        return f'({self.region}) {self.city} '

    def get_region(self):
        return self.region

    class Meta:
        unique_together = ('region', 'city')


class HeatingChoices(models.Model):
    """
    Class that represents the heating choices of a listings
    """
    name = models.CharField(_("Heating type"), max_length=255)

    def __str__(self):
        return self.name


class Listing(BaseModel):
    """
    A class that represents a listings. A listings can be a house or an apartment. A listings can be for selling or renting.
    """

    # Listing dependencies
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    city = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, related_name='listings')


    # Listing specification
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'))
    address = models.CharField(_('Address'), max_length=80, blank=True)
    zip_code = models.CharField(_('Zip-code'), max_length=10, validators=[RegexValidator(regex=REGEX_ZIPCODE_VALIDATOR, message='Zip code must be in format 1234AB', code='invalid_zipcode')])
    home_type = models.CharField(_('Type of home'), max_length=10, default='house', choices=HOME_TYPE, help_text=_('Designates the type of home: House or Apartment'))
    quadrature = models.PositiveSmallIntegerField(_('Quadrature'))
    rooms = models.PositiveSmallIntegerField(_('Rooms'))
    bedrooms = models.PositiveSmallIntegerField(_('Bedrooms'))
    floor = models.PositiveSmallIntegerField(_('Floor'))
    interior = models.CharField(max_length=255, choices=INTERIOR_CHOICES, default='unspecified')
    heating = models.ManyToManyField(HeatingChoices)
    price = models.DecimalField(_('Price in EUR'), max_digits=9, decimal_places=0)
    basement = models.BooleanField(_('Basement'), default=False)
    parking = models.BooleanField(_('Parking place'), default=False)
    elevator = models.BooleanField(_('Elevator'), default=False)
    balcony = models.BooleanField(_('Balcony'), default=False)

    # Listing data
    times_visited = models.PositiveIntegerField(_('Times visited'), default=0)
    is_available = models.BooleanField(_('Available?'), default=True)
    available_from = models.DateField(blank=True, null=True)
    rental_period = models.PositiveSmallIntegerField(_('Minimum rental period (in months)'), default=6, blank=True, null=True)
    is_approved = models.NullBooleanField(_('Approved?'), default=None)
    rejection_reason = models.CharField(_('Rejection reason'), max_length=255, null=True, blank=True)
    # @TODO: If the house is for selling - some fields should be deleted in the form
    listing_type = models.CharField(_('Listing type'), max_length=10, default='rent', choices=LISTING_TYPE, help_text=_('Designates the type of listings: rent or sell'))

    # Admin data
    soft_deleted = models.BooleanField(_('Soft deleted'), default=False)

    def __str__(self):
        return f"({self.zip_code}) {self.title}"


class Saved(models.Model):
    """
    A class used for saving listings for later
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='saved')

    def __str__(self):
        return f"{self.user} - {self.listing}"


class SearchProfiles(BaseModel):
    """
    A class used for saving user search profiles.
    Will be used for informing a user when a listings is in his listings criteria

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='searchprofiles')
    title = models.CharField(_("Search profile title"), max_length=255, blank=True, null=True)
    city = models.ForeignKey(Place, on_delete=models.DO_NOTHING, related_name='searchprofiles')
    listing_type = models.CharField(_('Listing type'), max_length=10, default='rent', choices=LISTING_TYPE_2, help_text=_('Designates the type of search profile: rent or sell'))
    rooms = models.PositiveSmallIntegerField(_("Minimum number of rooms"), default=1)
    bedrooms = models.PositiveSmallIntegerField(_("Minimum number of bedrooms"), default=1)
    price_from = models.PositiveIntegerField(_("Price from"), default=1)
    price_to = models.PositiveIntegerField(_("Price to"), default=1000)
    frequency = models.CharField(_("Update frequency"), choices=UPDATE_FREQUENCIES, default='weekly', max_length=255)

    def __str__(self):
        return f"{self.user} - {self.title}"

    def clean(self):
        if self.price_from > self.price_to:
            raise ValidationError({'price_from': "Price_from can not be smaller than price_to"})
        if self.rooms < self.bedrooms:
            raise ValidationError({'rooms': "You can not have less rooms than bedrooms"})

    def clean_fields(self, exclude=None):
        pass


class Comment(BaseModel):
    """
    A class that represent listings's comments
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(_('Comment body'))

    def __str__(self):
        return f"{self.body}"