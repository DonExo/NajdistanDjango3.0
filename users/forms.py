from django import forms
from django.utils.translation import gettext_lazy as _

from .form_widgets import SelectWidgetWithDisabledOption
from .models import User, SearchProfiles
from configdata import UPDATE_FREQUENCIES


class UserUpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'telephone', 'email', 'profile_image')


class UserSearchProfileForm(forms.ModelForm):
    frequency = forms.ChoiceField(required=True, widget=SelectWidgetWithDisabledOption, choices=UPDATE_FREQUENCIES)


    class Meta:
        model = SearchProfiles
        exclude = ('user', )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)


        if not self.user.is_staff:  #@TODO: Change this to PREMIUM user once the logic is there
            self.fields['frequency'].widget.disabled_choices = ['instant',]

            if self.user.has_search_profile():
                # Render all inputs as disabled
                for key, value in self.fields.items():
                    value.disabled = True


    def clean_title(self):
        title = self.cleaned_data['title']
        exists = SearchProfiles.objects.filter(user=self.user, title__iexact=title).exists()
        if exists:
            raise forms.ValidationError(_('You already have a Search Profile with this exact title.'))
        return title
