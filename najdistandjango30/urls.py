from django.contrib import admin
from django.urls import path, include, re_path

from backend import views

urlpatterns = [
    path('', views.index),

    path('admin/', admin.site.urls),
]
