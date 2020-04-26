from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from listings.views import ListingIndexView

urlpatterns = [
    path('', ListingIndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('listings/', include(('listings.urls', 'listings'), namespace='listings')),

    path('accounts/', include('registration.backends.default.urls')),

    path('user/', include(('users.urls', 'users'), namespace='accounts')),

    path('auth/', include(('authy.urls', 'authy'), namespace='authy')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns
#
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)