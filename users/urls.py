from django.urls import path
from users import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update, name='update_user'),
    path('profile/<slug:identifier>/', views.user_identifier, name='user_identifier'),

    # Search Profiles URLs
    path('sp/', views.search_profile_create, name='sp_create'),
    path('sp/update/', views.search_profile_create, name='sp_update'),
    path('sp/delete/', views.search_profile_create, name='sp_delete'),

]
