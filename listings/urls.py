from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.ListingSearchView.as_view(), name='search'),
    path('create/', views.ListingCreateView.as_view(), name='create'),
    path('compare/', views.ListingCompareView.as_view(), name='compare'),
    path('get_json_data/', views.ListingJsonData.as_view(), name='get_json'),

    # Slug related urls
    path('<slug:slug>/', views.ListingDetailView.as_view(), name='detail'),  # Remove the last slash if Django complains
    path('<slug:slug>/update/', views.ListingUpdateView.as_view(), name='update'),
    path('<slug:slug>/delete/', views.ListingDeleteView.as_view(), name='delete'),
    path('<slug:slug>/toggle_status/', views.ListingToggleStatusView.as_view(), name='update_status'),
]

