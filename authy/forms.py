from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, AuthenticationForm, UsernameField, PasswordChangeForm

from registration.forms import RegistrationFormTermsOfService
from users.models import User
from .captchas import CustomCaptchaV2Invisible


class CustomLoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.EmailInput(attrs={'autofocus': True}))
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    # captcha = CustomCaptchaV2Invisible()

    # Workaround for the "Inactive user error" to be shown on Login
    # This is a Django bug existing for 3 years already. Bug #28645
    # This also introduces an extra error_message for users who deleted their accounts.
    def clean(self):
        self.error_messages.update(
            {'inactive_deleted': 'You have deactivated your account. '
                                 'Click the "Forgot your password" link to activate it again,'}
        )
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(email=username)
                    check_pass = user_temp.check_password(password)
                    user = None
                    if check_pass:
                        user = user_temp
                except:
                    user = None
                if user is not None and not user.is_active:
                    self.confirm_login_allowed(user)
                raise self.get_invalid_login_error()
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        if user.soft_delete:
            raise forms.ValidationError(
                self.error_messages['inactive_deleted'],
                code='inactive_deleted',
            )
        else:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )


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
