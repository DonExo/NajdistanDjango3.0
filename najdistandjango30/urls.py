from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from users import views

urlpatterns = [
    path('', views.index),

    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls'))
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns