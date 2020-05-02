from django.forms.widgets import TextInput

import django_filters as filters

from .models import Listing, Place
from .filter_utils import MinMaxRangeWidget


class ListingFilter(filters.FilterSet):
    title = filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        widget=TextInput(
            attrs={'placeholder': 'Enter a keyword....'}
        )
    )
    price = filters.RangeFilter(
        field_name='price',
        widget=MinMaxRangeWidget(
            from_attrs={'placeholder': 'Min price (in EUR)'},
            to_attrs={'placeholder': 'Max price (in EUR)'}
        )
    )
    city = filters.ChoiceFilter(
        field_name='city',
        lookup_expr='exact',
        empty_label='All cities',
        choices=[(obj.pk, obj) for obj in Place.objects.all()],
    )

    class Meta:
        model = Listing
        fields = ['title', 'city', 'price']
