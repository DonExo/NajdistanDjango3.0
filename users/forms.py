from django import forms

from .models import User


class UserUpdateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, help_text="You need to enter your current password to make changes", )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'telephone', 'email', 'profile_image', )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_password(self):
        user = self.instance
        entered_password = self.cleaned_data['password']
        if not user.check_password(entered_password):
            raise forms.ValidationError("Incorrect password!")
        return entered_password
