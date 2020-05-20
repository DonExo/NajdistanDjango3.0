from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Listing


class ListingCreateForm(forms.ModelForm):
    images = forms.ImageField(widget = forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Listing
        fields = ('title', 'description', 'listing_type', 'home_type', 'city', 'zip_code',
                  'quadrature', 'rooms', 'bedrooms', 'floor', 'heating', 'price')
        # @TODO: Add all necessary values

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.startswith('a'):
            raise forms.ValidationError("Ne mojt so A da pocvit ;) ")
        return title

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].empty_label = _("Select a city")


class ListingUpdateForm(ListingCreateForm):
    title = forms.CharField(disabled=True)
