import hashlib
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from .utils import profile_image_directory_path

from configdata import LISTING_TYPE_2, UPDATE_FREQUENCIES, INTERIOR_CHOICES


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    """
    A base class that represents an instance of a logged-in User
    """
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True, blank=False)
    telephone = models.CharField(_('Phone number'), max_length=255)
    username = None
    profile_image = models.ImageField(upload_to=profile_image_directory_path, blank=True, null=True)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.get_full_name()

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def avatar(self):
        base_url = 'https://www.gravatar.com/avatar/'
        gravatar_url = base_url + hashlib.md5(self.email.lower().encode('utf-8')).hexdigest() + '?d=wavatar&s=100'
        return gravatar_url

    @property
    def get_profile_image(self):
        if self.profile_image:
            return self.profile_image.url
        return self.avatar

    def get_listings(self):
        return self.listings.prefetch_related('city').all()

    def get_absolute_url(self):
        return reverse('accounts:user_identifier', kwargs={'identifier': self.identifier})

    def get_search_profiles(self):
        return self.searchprofiles.prefetch_related('city').all()

    def has_search_profile(self):
        #@TODO: Change is_staff with PREMIUM user
        return not self.is_staff and self.searchprofiles.all().count() >= 1


class SearchProfiles(BaseModel):
    """
    A class used for saving user Search Profiles.
    Will be used for informing a user when a listings is in his listings criteria
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='searchprofiles')
    title = models.CharField(_("Name your Search Profile"), max_length=255, null=True)
    city = models.ForeignKey("listings.Place", on_delete=models.DO_NOTHING)
    listing_type = models.CharField(_('Listing type'), max_length=10, default='rent', choices=LISTING_TYPE_2, help_text=_('Designates the type of search profile: rent or sell'))
    rooms = models.PositiveSmallIntegerField(_("Number of rooms"), default=2)
    bedrooms = models.PositiveSmallIntegerField(_("Number of bedrooms"), default=1)
    min_price = models.DecimalField(_("Minimum price"), max_digits=9, decimal_places=0)
    max_price = models.DecimalField(_("Maximum price"),  max_digits=9, decimal_places=0)
    interior = models.CharField(max_length=15, choices=INTERIOR_CHOICES, default='unspecified')
    frequency = models.CharField(_("Update frequency"), choices=UPDATE_FREQUENCIES, default='weekly', max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'title')

    def __str__(self):
        return self.title

    def clean(self):
        if self.rooms < self.bedrooms:
            raise ValidationError({'rooms': "You can not have less rooms than bedrooms"})
        if self.min_price > self.max_price:
            raise ValidationError({'min_price': "Minimum price can't be bigger than maximum price"})

