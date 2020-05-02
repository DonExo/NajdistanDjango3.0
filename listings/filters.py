import django_filters as filters

from django.forms.widgets import TextInput

from django_filters.widgets import RangeWidget

from .models import Listing

class ListingFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains', widget=TextInput(attrs={'placeholder': 'Enter address e.g. street, city and state or zip'}))
    price = filters.RangeFilter(field_name='price', label='Price range', widget=RangeWidget(attrs={'placeholder': 'Price range'}))

    #@TODO: Make sure to add all the needed filters with right properties (i.e. quadrature, balcony etc)

    class Meta:
        model = Listing
        fields = ('title', 'city', 'price')