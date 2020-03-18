import hashlib

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from .configs import LISTING_TYPE, HOME_TYPE, REGEX_ZIPCODE_VALIDATOR, INTERIOR_CHOICES, UPDATE_FREQUENCIES


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
    # is_active = False
    # profile_image = models.ImageField(upload_to=image_profiles_directory_path, default=None, blank=True, null=True)

    def __str__(self):
        return self.get_full_name() or self.email

    def get_absolute_url(self):
        # return reverse('view:user-detail', args=[self.pk])
        pass

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def avatar(self):
        base_url = 'https://www.gravatar.com/avatar/'
        gravatar_url = base_url + hashlib.md5(self.email.lower().encode('utf-8')).hexdigest() + '?d=wavatar&s=100'
        # if self.profile_image:
        #     return self.profile_image.url
        return gravatar_url


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

    # def get_cities_by_region(self, value):
    #     pass


class HeatingChoices(models.Model):
    """
    Class that represents the heating choices of a listing
    """
    name = models.CharField(_("Heating type"), max_length=255)

    def __str__(self):
        return self.name


class Listing(BaseModel):
    """
    A class that represents a listing. A listing can be a house or an apartment. A listing can be for selling or renting.
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
    listing_type = models.CharField(_('Listing type'), max_length=10, default='rent', choices=LISTING_TYPE, help_text=_('Designates the type of listing: rent or sell'))

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
    Will be used for informing a user when a listing is in his listing criteria

    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='searchprofiles')
    title = models.CharField(_("Search profile title"), max_length=255, blank=True, null=True)
    city = models.ForeignKey(Place, on_delete=models.DO_NOTHING, related_name='searchprofiles')
    rooms = models.PositiveSmallIntegerField(_("Minimum number of rooms"), default=1)
    bedrooms = models.PositiveSmallIntegerField(_("Minimum number of bedrooms"), default=1)
    price_from = models.DecimalField(max_digits=9, decimal_places=0)
    price_to = models.DecimalField(max_digits=9, decimal_places=0)
    frequency = models.CharField(_("Update frequency"), choices=UPDATE_FREQUENCIES, default='weekly', max_length=255)

    def __str__(self):
        return f"{self.user} - {self.title}"


class Comment(BaseModel):
    """
    A class that represent listing's comments
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField(_('Comment body'))

    def __str__(self):
        return f"{self.text}"


class CommentReport(BaseModel):
    """
    A class that represents a report of a comment
    """
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='commentreports')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='commentreports')
    reason = models.TextField(_('Reason for reporting this comment'), blank=True, null=True)

    def __str__(self):
        return f"{self.comment} - {self.user}"


class ListingReport(BaseModel):
    """
    A class that represents a report of a listing
    """
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='listingreports')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listingreports')
    reason = models.TextField(_('Reason for reporting this listing'), blank=True, null=True)

    def __str__(self):
        return f"{self.listing} - {self.user}"


