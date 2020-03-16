import hashlib

from django.db import models
from django.urls import reverse

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True, blank=False)
    telephone = models.CharField(_('Phone number'), max_length=255)
    username = None
    # last_seen = models.DateTimeField(auto_now=True) # for this it can be used 'last_login'
    # profile_image = models.ImageField(upload_to=image_profiles_directory_path, default=None, blank=True, null=True)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        # return reverse('view:user-detail', args=[self.pk])
        pass

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def avatar(self):
        base_url = "https://www.gravatar.com/avatar/"
        gravatar_url = base_url + hashlib.md5(self.email.lower().encode('utf-8')).hexdigest() + "?d=wavatar&s=100"
        # if self.profile_image:
        #     return self.profile_image.url
        return gravatar_url