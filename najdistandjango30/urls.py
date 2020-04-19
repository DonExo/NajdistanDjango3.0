from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from listings.views import ListingListView

urlpatterns = [
    path('', ListingListView.as_view(), name='list'),
    path('admin/', admin.site.urls),
    path('listings/', include(('listings.urls', 'listings'), namespace='listings')),
    path('accounts/', include('registration.backends.default.urls')),
    path('accounts/', include(('users.urls', 'users'), namespace='accounts')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns
#
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# accounts/ ^activate/complete/$ [name='registration_activation_complete']
# accounts/ ^activate/resend/$ [name='registration_resend_activation']
# accounts/ ^activate/(?P<activation_key>\w+)/$ [name='registration_activate']
# accounts/ ^register/complete/$ [name='registration_complete']
# accounts/ ^register/closed/$ [name='registration_disallowed']
# accounts/ ^register/$ [name='registration_register']
# accounts/ ^login/$ [name='auth_login']
# accounts/ ^logout/$ [name='auth_logout']
# accounts/ ^password/change/$ [name='auth_password_change']
# accounts/ ^password/change/done/$ [name='auth_password_change_done']
# accounts/ ^password/reset/$ [name='auth_password_reset']
# accounts/ ^password/reset/complete/$ [name='auth_password_reset_complete']
# accounts/ ^password/reset/done/$ [name='auth_password_reset_done']
# accounts/ ^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$ [name='auth_password_reset_confirm']