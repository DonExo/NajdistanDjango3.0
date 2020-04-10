
from django.urls import path

from listings import views


urlpatterns = [
    path('', views.ListingListView.as_view(), name='list'),
    path('create/', views.ListingCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.ListingDetailView.as_view(), name='detail'), # Remove the last slash if Django complains
    path('<slug:slug>/update/', views.ListingUpdateView.as_view(), name='update'),
    # path('detail/<int:pk>/delete/', views.ListingDetailView.as_view(), name='delete'),
    path('<slug:slug>/delete/', views.delete_listing, name='delete'),
]