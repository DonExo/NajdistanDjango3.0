from dal import autocomplete
from django import forms

from .models import Listing


class ListingCreateForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('title', 'description', 'listing_type', 'city', 'home_type', 'zip_code', 'quadrature',
                  'rooms', 'bedrooms', 'floor', 'heating', 'price', 'cover_image')
        # @TODO: Add all necessary values
        widgets = {
            'city': autocomplete.ModelSelect2(url='listings:city-autocomplete')
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.startswith('a'):
            raise forms.ValidationError("Ne mojt so A da pocvit ;) ")
        return title


class ListingUpdateForm(ListingCreateForm):
    title = forms.CharField(disabled=True)
