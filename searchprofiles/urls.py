from django.urls import path
from . import views


urlpatterns = [
    path('create/',             views.search_profile_create,            name='create'),
    path('update/<int:pk>/',    views.search_profile_update,            name='update'),
    path('delete/<int:pk>/',    views.search_profile_delete,            name='delete'),
    path('toggle/<int:pk>/',    views.search_profile_toggle_status,     name='toggle'),
]