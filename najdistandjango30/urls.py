from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from listings.views import ListingIndexView

from authy.views import LoginView


urlpatterns = [
    path('',            ListingIndexView.as_view(), name='index'),
    path('listings/',   include(('listings.urls', 'listings'), namespace='listings')),
    path('accounts/',   include('registration.backends.default.urls')),  # Used only for the Activation part
    path('user/',       include(('users.urls', 'users'), namespace='accounts')),
    path('auth/',       include(('authy.urls', 'authy'), namespace='authy')),
    path('sp/',         include(('searchprofiles.urls', 'searchprofiles'), namespace='searchprofiles')),
    path('office/',     admin.site.urls),

    # Hack alert, this is needed for the ?next issue when changing the 'auth_login'..
    path('login/',      LoginView.as_view(), name='auth_login'),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns
#
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)