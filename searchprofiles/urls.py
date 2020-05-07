from django.urls import path
from . import views


urlpatterns = [
    path('sp/', views.search_profile_create, name='sp_create'),
    path('sp/update/<int:pk>/', views.search_profile_update, name='sp_update'),
    path('sp/delete/<int:pk>/', views.search_profile_delete, name='sp_delete'),
    path('sp/toggle/<int:pk>/', views.toggle_sp_status, name='sp_toggle'),
]