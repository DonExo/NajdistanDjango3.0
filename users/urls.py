from django.urls import path
from . import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('properties/', views.properties, name='properties'),
    path('bookmarks/', views.bookmarks, name='bookmarks'),
    path('deactivate/', views.deactivate_account, name='deactivate'),
    path('profile/update/', views.update, name='profile_update'),
    path('publisher/<slug:identifier>/', views.publisher, name='publisher'),
]
