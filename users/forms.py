from django import forms

from .models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'telephone', 'email', 'profile_image')
