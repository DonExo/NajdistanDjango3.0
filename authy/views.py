from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.generic import RedirectView

from registration.backends.default.views import RegistrationView

from authy.forms import CustomPasswordResetForm, CustomRegisterForm, CustomLoginForm, CustomPasswordChangeForm
from configdata import LOGIN_COOKIE_EXPIRY


class LoginView(auth_views.LoginView):
    redirect_authenticated_user = True
    form_class = CustomLoginForm
    extra_context = {'title': _('Log in')}

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me', None)
        auth_login(self.request, form.get_user())
        messages.info(self.request, _("You've successfully logged in!"))
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
    success_url = 'authy:register_complete'
    disallowed_url = 'authy:register_closed'
    extra_context = {'title': _('Register')}


class PasswordChangeView(auth_views.PasswordChangeView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('authy:password_change_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Change Password')
        context['crumbs'] = {
            "Home": reverse('index'),
            "Account": reverse('accounts:profile'),
            "Password": '#',
        }
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
    form_class = CustomPasswordResetForm
    redirect_authenticated_user = True
    extra_context = {'title': _('Password reset')}
    success_url = reverse_lazy('authy:password_reset_done')
    html_email_template_name = 'registration/password_reset_email.html'

    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Prevent accessing the URL if user is authenticated
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            messages.error(request, _("You can not access this route if you are logged in!"))
            return redirect(reverse('accounts:profile'))
        return super().dispatch(request, *args, **kwargs)


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy('authy:password_reset_complete')
    extra_context = {'title': _('Set new password')}
