from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "Please log-in to perform that action.")
        return super().dispatch(request, *args, **kwargs)
