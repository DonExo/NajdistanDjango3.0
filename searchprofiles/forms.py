from django import forms

from django.utils.translation import gettext_lazy as _

from .form_widgets import SelectWidgetWithDisabledOption
from .models import SearchProfiles
from configdata import UPDATE_FREQUENCIES, HOME_TYPE, INTERIOR_CHOICES


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
        self.fields['home_type'] = forms.ChoiceField(choices=HOME_TYPE)
        self.fields['interior'] = forms.ChoiceField(choices=INTERIOR_CHOICES)
        self.fields['listing_type'] = forms.ChoiceField(choices=[('rent', 'To rent'), ('buy', 'To buy')])
        # TODO: Might need to change 'buy' to 'sell' for easier DB query

        if not self.user.is_premium_user:
            self.fields['frequency'].widget.disabled_choices = ['instant',]
            for field in ['interior', 'home_type', 'rooms', 'bedrooms']:
                self.fields[field].widget.attrs['disabled'] = 'disabled'
                self.fields[field].required = False

            if not self.is_updating and self.user.has_search_profile():
                for key, value in self.fields.items():
                    value.disabled = True

    def clean_title(self):
        title = self.cleaned_data['title']
        exists = SearchProfiles.objects.exclude(pk=self.instance.pk).filter(user=self.user, title__iexact=title).exists()
        if exists:
            raise forms.ValidationError(_('You already have a Search Profile with this exact Title.'))
        return title

    def clean_frequency(self):
        frequency = self.cleaned_data['frequency']
        if frequency == 'instant' and not self.user.is_premium_user:
            raise forms.ValidationError(_("Upgrade to Premium use to use this feature"))
        return frequency
