from datetime import datetime

from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import F
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from configdata import REGEX_ZIPCODE_VALIDATOR, HOME_TYPE, INTERIOR_CHOICES, LISTING_TYPE, HEATING_CHOICES
from users.models import BaseModel, User
from users.utils import listing_image_directory_path
from .managers import CustomListingQuerySet


class Place(models.Model):
    """
    A class that represents a place/region
    """
    region = models.CharField(_('Region'), max_length=255)
    city = models.CharField(_('City'), max_length=255)

    def __str__(self):
        return self.city

    def get_region(self):
        return self.region

    class Meta:
        unique_together = ('region', 'city')


class Listing(BaseModel):
    """
    A class that represents a listings. A listings can be a house or an apartment. A listings can be for selling or renting.
    """

    # Listing dependencies
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='listings')
    city = models.ForeignKey('listings.Place', on_delete=models.SET_NULL, null=True, related_name='listings')

    # Listing specification
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'))
    address = models.CharField(_('Address'), max_length=80, blank=True)
    zip_code = models.CharField(_('Zip-code'), max_length=10, validators=[
        RegexValidator(regex=REGEX_ZIPCODE_VALIDATOR, message='Zip code must be in format 1234AB', code='invalid_zipcode')])

    # Choices fields
    home_type = models.CharField(_('Type of home'), max_length=10, default='apartment', choices=HOME_TYPE)
    listing_type = models.CharField(_('Listing type'), max_length=10, default='rent', choices=LISTING_TYPE)
    interior = models.CharField(max_length=255, default='unfurnished', choices=INTERIOR_CHOICES)
    heating = models.CharField(max_length=50, choices=HEATING_CHOICES, default='Gas')

    # Numbers fields
    quadrature = models.PositiveSmallIntegerField(_('Quadrature'))
    rooms = models.PositiveSmallIntegerField(_('Rooms'))
    bedrooms = models.PositiveSmallIntegerField(_('Bedrooms'))
    floor = models.PositiveSmallIntegerField(_('Floor'), null=True, blank=True)
    price = models.DecimalField(_('Price in EUR'), max_digits=9, decimal_places=0)
    construction_year = models.IntegerField(_('Construction Year'),
                                            validators=[MinValueValidator(1900), MaxValueValidator(2020)], null=True)

    # Checkbox fields
    basement = models.BooleanField(_('Basement'), default=False)
    parking = models.BooleanField(_('Parking place'), default=False)
    elevator = models.BooleanField(_('Elevator'), default=False)
    balcony = models.BooleanField(_('Balcony'), default=False)

    # Listing admin data
    is_approved = models.NullBooleanField(_('Approved?'), default=None)
    is_available = models.BooleanField(_('Available?'), default=True)
    rejection_reason = models.CharField(_('Rejection reason'), max_length=255, null=True, blank=True)
    available_from = models.DateField(blank=True, null=True)
    rental_period = models.PositiveSmallIntegerField(_('Minimum rental period (in months)'), default=6, blank=True, null=True)
    times_visited = models.PositiveIntegerField(_('Times visited'), default=0)
    soft_deleted = models.BooleanField(_('Soft deleted'), default=False)
    slug = models.SlugField(max_length=255, unique=True)

    objects = CustomListingQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at', ]

    def __str__(self):
        return self.slug

    def get_images(self):
        return self.images.all()

    def get_cover_image(self):
        if self.get_images():
            return self.images.first().image

    def get_images_count(self):
        return int(self.images.all().count())

    def get_absolute_url(self):
        return reverse('listings:detail', kwargs={'slug': self.slug})

    def get_bookmarked_by(self):
        return self.bookmarked_by.all()

    def is_active(self):
        return self.is_available and self.is_approved

    def toggle_status(self):
        self.is_available = not self.is_available
        self.save()

    def save(self, *args, **kwargs):
        if not self.id:
            # Let's create unique slug for the article
            date_time_object = datetime.utcnow().strftime("%d%m%Y%H%M%S")
            self.slug = "-".join([slugify(self.title), date_time_object])
        super().save(*args, **kwargs)

    # This ensures that all related images are deleted from the system
    def delete(self, using=None, keep_parents=False):
        for image in self.images.all():
            image.delete()
            image.image.storage.delete(image.image.name)
        super().delete()


class Image(BaseModel):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=listing_image_directory_path)
    order = models.PositiveSmallIntegerField(default=1, blank=True, null=True)

    def __str__(self):
        return self.image.name


class Saved(models.Model):
    """
    A class used for saving listings for later
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='saved')

    def __str__(self):
        return f"{self.user} - {self.listing}"


class Comment(BaseModel):
    """
    A class that represent listings's comments
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(_('Comment body'))

    def __str__(self):
        return f"{self.body}"
