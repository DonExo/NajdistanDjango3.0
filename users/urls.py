from django.urls import path
from users import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update, name='update_user'),
    path('profile/<slug:identifier>/', views.user_identifier, name='user_identifier'),

]
