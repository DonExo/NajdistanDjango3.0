
from django.urls import path

from listings import views


urlpatterns = [
    path('', views.ListingListView.as_view(), name='list'),
    path('create/', views.ListingCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ListingDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.ListingUpdateView.as_view(), name='update'),
    # path('detail/<int:pk>/delete/', views.ListingDetailView.as_view(), name='delete'),
    path('<int:pk>/delete/', views.delete_listing, name='delete'),
]
