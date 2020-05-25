from django import forms

from django.utils.translation import gettext_lazy as _

from .form_widgets import SelectWidgetWithDisabledOption
from .models import SearchProfiles
from configdata import UPDATE_FREQUENCIES


class UserSearchProfileForm(forms.ModelForm):
    title = forms.CharField(label='Name your Search Profile', help_text='A unique title that will mean something to you')
    frequency = forms.ChoiceField(required=True, widget=SelectWidgetWithDisabledOption, choices=UPDATE_FREQUENCIES,
                                 help_text='How often to receive notifications about new properties on our site')

    class Meta:
        model = SearchProfiles
        exclude = ('user', 'is_active')

        # To comply with the Index page Min-Max slider
        widgets = {
            'min_price': forms.NumberInput(attrs={'id': 'id_price_0'}),
            'max_price': forms.NumberInput(attrs={'id': 'id_price_1'}),
            'title': forms.TextInput(attrs={'placeholder': 'i.e. New apartment 50k-100k range, 2 bedrooms'})
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.is_updating = kwargs.pop('update', None)
        super().__init__(*args, **kwargs)
        self.fields['city'].empty_label = _("Select a City")

        if not self.user.is_staff:  #TODO: Change this to PREMIUM user once the logic is there
            self.fields['frequency'].widget.disabled_choices = ['instant',]
            if not self.is_updating and self.user.has_search_profile():
                for key, value in self.fields.items():
                    value.disabled = True

    def clean_title(self):
        title = self.cleaned_data['title']
        exists = SearchProfiles.objects.exclude(pk=self.instance.pk).filter(user=self.user, title__iexact=title).exists()
        if exists:
            raise forms.ValidationError(_('You already have a Search Profile with this exact title.'))
        return title

    def clean_frequency(self):
        frequency = self.cleaned_data['frequency']
        if frequency == 'instant' and not self.user.is_staff: # TODO: Here too!
            raise forms.ValidationError(_("Please upgrade to Premium use to user this feature"))
        return frequency
