from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic import RedirectView


class LoginView(auth_views.LoginView):
    template_name = "authy/login.html"
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log-in'
        return context

    def get_success_url(self):
        url = super().get_success_url()
        messages.info(self.request, _("You've successfully logged in!"))
        return url


class LogoutView(auth_views.LogoutView):
    redirect_unauthenticated_user = True

    def get_next_page(self):
        next_page = super().get_next_page()
        messages.info(self.request, _("You've been logged out!"))
        return next_page

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Prevent accessing the URL if user is not authenticated
        if self.redirect_unauthenticated_user and not self.request.user.is_authenticated:
            messages.error(request, _("You can not access this route if you are not logged in!"))
            return HttpResponseRedirect('/')
        return super().dispatch(request, *args, **kwargs)


class PasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'authy/password-change.html'
    success_url = reverse_lazy('authy:password_change_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Password change'
        return context


class PasswordChangeDoneView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('accounts:profile')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        messages.info(self.request, _("You password has been changed!"))
        self.send_password_change_confirmation_email()
        return super().dispatch(request, *args, **kwargs)

    def send_password_change_confirmation_email(self):
        # TODO: Add the e-mail confirmation here
        print("Email confirmation: Password changed!")