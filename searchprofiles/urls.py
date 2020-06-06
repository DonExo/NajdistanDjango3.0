from django.urls import path
from . import views


urlpatterns = [
    path('manage/',             views.search_profile_manage,    name='manage'),
    path('create/',             views.search_profile_create,    name='create'),
    path('toggle/',             views.search_profile_toggle,    name='toggle'),
    path('update/<int:pk>/',    views.search_profile_update,    name='update'),
    path('delete/<int:pk>/',    views.search_profile_delete,    name='delete'),
]
