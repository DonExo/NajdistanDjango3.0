from django.contrib import admin
from django.urls import path, include, re_path

from users import views

urlpatterns = [
    path('', views.index),

    path('admin/', admin.site.urls),
]
