from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm, UsernameField, PasswordChangeForm

from registration.forms import RegistrationFormTermsOfService
from users.models import User
from .captchas import CustomCaptchaV2Invisible


class CustomLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.EmailInput(attrs={'autofocus': True}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    captcha = CustomCaptchaV2Invisible()

    # Workaround for the "Inactive user error" to be shown on Login
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(email=username)
                except:
                    user_temp = None
                if user_temp is not None:
                    self.confirm_login_allowed(user_temp)
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )
        return self.cleaned_data

class CustomRegisterForm(RegistrationFormTermsOfService):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    telephone = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'telephone')


class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        exists = User.objects.filter(email=email).exists()
        if not exists:
            raise forms.ValidationError("User does not exists!")
        return email


class CustomPasswordChangeForm(PasswordChangeForm):
    pass

