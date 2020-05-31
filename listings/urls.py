from django.urls import path

from . import views

urlpatterns = [
    path('compare/', views.ListingCompareView.as_view(), name='compare'),
    path('search/', views.ListingSearchView.as_view(), name='search'),
    path('create/', views.ListingCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.ListingDetailView.as_view(), name='detail'),  # Remove the last slash if Django complains
    path('<slug:slug>/update/', views.ListingUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', views.ListingDeleteView.as_view(), name='delete'),
]
