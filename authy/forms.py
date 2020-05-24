from django import forms
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm, UsernameField

from registration.forms import RegistrationFormTermsOfService
from users.models import User
from .captchas import CustomCaptchaV2Invisible


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
    telephone = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'telephone')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    # def clean(self):
    #     cleaned_data = super().clean()


class CustomLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.EmailInput(attrs={'autofocus': True}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    captcha = CustomCaptchaV2Invisible()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
