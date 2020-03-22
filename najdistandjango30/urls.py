from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path

from users import views

urlpatterns = [
    path('', views.index, name='index'),

    path('admin/', admin.site.urls),

    path('accounts/', include('registration.backends.default.urls')),
]


# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
# ] + urlpatterns