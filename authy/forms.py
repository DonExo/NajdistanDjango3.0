from django import forms
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm

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


class CustomLoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    captcha = CustomCaptchaV2Invisible()

    #PLEASE LET THESE STAY AS REFERENCE FOR FUTURE FORM CHANGES
    #
    # username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class': 'igorce'}))
    # def __init__(self, *args, **kwargs):
    #     super(CustomLoginForm, self).__init__(*args, **kwargs)
    #     self.fields['password'].widget.attrs.update({'class' : 'password'})
    #     self.fields['remember_me'].widget.attrs.update({'class' : 'rememberme'})