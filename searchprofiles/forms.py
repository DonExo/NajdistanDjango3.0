from django import forms
from django.utils.translation import gettext_lazy as _

from .form_widgets import SelectWidgetWithDisabledOption
from .models import SearchProfiles
from configdata import UPDATE_FREQUENCIES, HOME_TYPE, INTERIOR_CHOICES

_premium_fields = ['interior', 'home_type', 'rooms', 'bedrooms']


class UserSearchProfileForm(forms.ModelForm):
    title = forms.CharField(label='Name your Search Profile', help_text='A unique title that will mean something to you', max_length=255, )
    frequency = forms.ChoiceField(required=True, widget=SelectWidgetWithDisabledOption, choices=UPDATE_FREQUENCIES,
                                 help_text='How often to receive notifications about new properties', initial='biweekly')

    class Meta:
        model = SearchProfiles
        exclude = ('user', 'is_active')

        # To comply with the Index page Min-Max slider
        widgets = {
            'min_price': forms.NumberInput(attrs={'id': 'id_price_0'}),
            'max_price': forms.NumberInput(attrs={'id': 'id_price_1'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.is_updating = kwargs.pop('update', None)
        super().__init__(*args, **kwargs)
        self.fields['city'].empty_label = None
        self.fields['home_type'] = forms.ChoiceField(choices=HOME_TYPE, required=False)
        self.fields['interior'] = forms.ChoiceField(choices=INTERIOR_CHOICES, required=False)
        self.fields['listing_type'] = forms.ChoiceField(choices=[('rent', 'To rent'), ('buy', 'To buy')])
        # TODO: Might need to change 'buy' to 'sell' for easier DB query

        if not self.user.is_premium_user:
            self.fields['frequency'].widget.disabled_choices = ['instant',]
            for field in _premium_fields:
                self.fields[field].widget.attrs['disabled'] = 'disabled'
                self.fields[field].required = False

            if not self.is_updating and self.user.has_reached_max_number_of_sp():
                for key, value in self.fields.items():
                    value.disabled = True

    def clean_title(self):
        title = self.cleaned_data['title']
        exists = SearchProfiles.objects.exclude(pk=self.instance.pk).filter(user=self.user, title__iexact=title).exists()
        if exists:
            raise forms.ValidationError(_('You already have a Search Profile with this exact Title.'))
        return title

    def clean(self):
        cleaned_data = super().clean()

        # Make sure the non-Premium user does not tamper the form manually,
        # by enabling a Premium field-only and add value to it
        if not self.user.is_premium_user:
            if cleaned_data['frequency'] == 'instant':
                self.add_error('frequency', "This is a Premium feature!")
            for field in _premium_fields:
                if cleaned_data[field]:
                    self.add_error(field, "This is a Premium feature!")
        return cleaned_data
