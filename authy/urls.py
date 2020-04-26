from django.urls import path, re_path
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

from authy import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),

    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('register/', views.RegisterView.as_view(), name='register'),

    path('register/complete/', TemplateView.as_view(
        template_name='authy/register_complete.html',
        extra_context={'title': _('Registration complete')},
    ), name='register_complete'),

    path('register/closed/', TemplateView.as_view(
        template_name='authy/register_closed.html',
        extra_context={'title': _('Registration closed')},
    ), name='register_closed'),

    path('pw/change/', views.PasswordChangeView.as_view(), name='password_change'),

    path('pw/change-done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('pw/reset/', views.PasswordResetView.as_view(), name='password_reset'),

    path('pw/reset-done/', TemplateView.as_view(
        template_name = 'authy/password-reset-done.html',
        extra_context={'title': _('Password reset initiated')},
    ), name='password_reset_done'),

    path('pw/reset-complete/', TemplateView.as_view(
        template_name='authy/password_reset_complete.html',
        extra_context={'title': _("Password reset completed")},
    ), name='password_reset_complete'),

    re_path(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
            views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
