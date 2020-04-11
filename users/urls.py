from django.urls import path
from users import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update, name='update_user'),
    path('profile/<slug:identifier>/', views.user_identifier, name='user_identifier'),

    # Search Profiles URLs
    path('sp/', views.search_profile_create, name='sp_create'),
    path('sp/update/<int:pk>/', views.search_profile_update, name='sp_update'),
    path('sp/delete/<int:pk>/', views.search_profile_delete, name='sp_delete'),

]
