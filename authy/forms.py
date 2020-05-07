from django import forms
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm

from captcha.fields import ReCaptchaField

from registration.forms import RegistrationFormTermsOfService

from users.models import User


class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        exists = User.objects.filter(email=email).exists()
        if not exists:
            raise forms.ValidationError("User does not exists!")
        return email


class CustomRegisterForm(RegistrationFormTermsOfService):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    telephone = forms.CharField(max_length=100) # TODO: Look for some validation

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'telephone')


class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    captcha = ReCaptchaField()