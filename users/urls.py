from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('properties/', views.properties, name='properties'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('profile/update/', views.update, name='profile_update'),
    path('profile/<slug:identifier>/', views.user_identifier, name='user_identifier'),
]
