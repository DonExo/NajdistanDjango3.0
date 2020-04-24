from django.contrib import messages
from django.contrib.auth import views as auth_views


class LoginView(auth_views.LoginView):
    template_name = "authy/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Log-in'
        return context


class LogoutView(auth_views.LogoutView):
    def get_next_page(self):
        next_page = super().get_next_page()
        messages.info(self.request, "You've been logged out!")
        return next_page