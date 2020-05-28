import hashlib
import uuid

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from configdata import REGEX_TELEPHONE_VALIDATOR
from .managers import CustomUserManager
from .utils import profile_image_directory_path


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    """
    A base class that represents an instance of a logged-in User
    """
    first_name = models.CharField(max_length=255, blank=False, validators=[MinLengthValidator(2)])
    last_name = models.CharField(max_length=255, blank=False, validators=[MinLengthValidator(2)])
    email = models.EmailField(unique=True, blank=False)
    telephone = models.CharField(_('Phone number'), max_length=255,
                                 validators=[RegexValidator(REGEX_TELEPHONE_VALIDATOR,
                                 message="Phone number should be a combination of numbers and '+' sign (i.e. +31612341234 or 0612341234)")])
    username = None
    profile_image = models.ImageField(upload_to=profile_image_directory_path, blank=True, null=True)
    identifier = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    soft_delete = models.BooleanField(null=True, default=False)

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

    # TODO: Check queries here!
    def get_listings(self):
        return self.listings.prefetch_related('city').all()

    def get_absolute_url(self):
        return reverse('accounts:user_identifier', kwargs={'identifier': self.identifier})

    @property
    def is_premium_user(self):
        return self.is_staff  # TODO: To be replaced with real logic about being Premium user

    def get_search_profiles(self):
        return self.searchprofiles.prefetch_related('city').all().order_by('-created_at')

    def has_search_profile(self):
        return not self.is_premium_user and self.searchprofiles.all().count() >= 1

    def get_bookmarks(self):
        return self.bookmarks.all()

    def deactivate(self):
        self.is_active = False
        self.soft_delete = True
        self.save()


class Bookmarks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    listing = models.ForeignKey('listings.Listing', on_delete=models.CASCADE, related_name='bookmarked_by')

    class Meta:
        verbose_name_plural = 'Bookmarks'

    def __str__(self):
        return f"{self.user} - {self.listing}"

    def clean(self):
        if self.user.pk == self.listing.user.pk:
            raise ValidationError("You can't bookmark your own listing!")

