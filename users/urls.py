from django.urls import path
from users import views


urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.update, name='update_user'),
]
