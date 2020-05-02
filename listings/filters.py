import django_filters as filters

from django.forms.widgets import TextInput

from .models import Listing
from .filter_utils import MinMaxRangeWidget


class ListingFilter(filters.FilterSet):
    title = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        widget=TextInput(
            attrs={'placeholder': 'zelka'}
        )
    )
    price = filters.RangeFilter(
        field_name='price',
        widget=MinMaxRangeWidget(
            from_attrs={'placeholder': 'melka'},
            to_attrs={'placeholder': 'kelka'}
        )
    )

    # city = filters.ChoiceFilter(field_name='city',  widget=Select(attrs={'placeholder': 'city'}))
    #@TODO: Make sure to add all the needed filters with right properties (i.e. quadrature, balcony etc)

    class Meta:
        model = Listing
        fields = ('title', 'city', 'price')