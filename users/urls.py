from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/properties/', views.properties, name='properties'),
    path('profile/update/', views.update, name='profile_update'),
    path('profile/<slug:identifier>/', views.user_identifier, name='user_identifier'),
]
