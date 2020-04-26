from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic import RedirectView

from registration.backends.default.views import RegistrationView

from authy.forms import CustomPasswordResetForm, CustomRegisterForm, CustomLoginForm
from configdata import LOGIN_COOKIE_EXPIRY


class LoginView(auth_views.LoginView):
    template_name = "authy/login.html"
    redirect_authenticated_user = True
    form_class = CustomLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Log-in')
        return context

    def get_success_url(self):
        url = super().get_success_url()
        messages.info(self.request, _("You've successfully logged in!"))
        return url

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me', None)
        auth_login(self.request, form.get_user())
        if remember_me:
            self.request.session.set_expiry(LOGIN_COOKIE_EXPIRY)
        return super().form_valid(form)


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


class RegisterView(RegistrationView):
    form_class = CustomRegisterForm
    redirect_authenticated_user = True
    template_name = 'authy/register.html'
    success_url = 'authy:register_complete'
    disallowed_url = 'authy:register_closed'
    extra_context = {'title': _('Register')}


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


class PasswordResetView(auth_views.PasswordResetView):
    template_name = 'authy/password-reset.html'
    email_template_name = 'authy/password_reset_email.html'
    success_url = reverse_lazy('authy:password_reset_done')
    redirect_authenticated_user = True
    form_class = CustomPasswordResetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Password reset')
        return context

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Prevent accessing the URL if user is not authenticated
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            messages.error(request, _("You can not access this route if you are logged in!"))
            return HttpResponseRedirect('/user/profile/')
        return super().dispatch(request, *args, **kwargs)


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy('authy:password_reset_complete')
    template_name = 'authy/password_reset_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Set new password')
        return context
