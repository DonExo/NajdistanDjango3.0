import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

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
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(unique=True, blank=False)
    telephone = models.CharField(_('Phone number'), max_length=255)
    username = None
    profile_image = models.ImageField(upload_to=profile_image_directory_path, default=None, blank=True, null=True)

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





