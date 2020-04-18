
from django.urls import path

from listings import views
from .widgets import CityAutocomplete
from .models import Place, Listing


urlpatterns = [
    path('city-autocomplete/', CityAutocomplete.as_view(), name='city-autocomplete'),  # needs to be before the detail view

    path('', views.ListingListView.as_view(), name='list'),
    path('create/', views.ListingCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.ListingDetailView.as_view(), name='detail'),  # Remove the last slash if Django complains
    path('<slug:slug>/update/', views.ListingUpdateView.as_view(), name='update'),
    path('<slug:slug>/upload/', views.ListingUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', views.ListingDeleteView.as_view(), name='delete'),
]
