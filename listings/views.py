from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Listing
from .forms import ListingCreateForm, ListingUpdateForm
from configdata import FORBIDDEN_MESAGE


class ListingListView(generic.ListView):
    # queryset = Listing.objects.approved()
    queryset = Listing.objects.all()
    template_name = 'listings/list.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return self.queryset.prefetch_related('user', 'city')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['foo'] = 'bar'  # Let's add something to the context
        return context

class ListingCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    login_url = reverse_lazy('auth_login')
    model = Listing
    template_name = 'listings/create.html'
    form_class = ListingCreateForm
    success_message = "Listing successfully created!"

    def get_success_url(self):
        return reverse_lazy('listings:detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ListingDetailView(generic.DetailView):
    model = Listing
    template_name = 'listings/detail.html'
    queryset = Listing.objects.select_related('user')


class ListingUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Listing
    template_name = 'listings/update.html'
    form_class = ListingUpdateForm
    permission_denied_message = FORBIDDEN_MESAGE

    def get_success_url(self):
        return reverse_lazy('listings:detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        return super().form_valid(form)

    # Checks if the listing owner is different than the request user
    def test_func(self):
        return self.request.user == self.get_object().user


class ListingDeleteView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        listing = get_object_or_404(Listing, slug=self.kwargs.get('slug'))
        if listing.user != self.request.user:
            messages.error(self.request, FORBIDDEN_MESAGE)
            return reverse('listings:detail', kwargs={'slug': listing.slug})
            # return HttpResponseForbidden(FORBIDDEN_MESAGE)  # This raises error otherwise
        listing.delete()
        messages.info(self.request, "Deleted listing!")
        return reverse('accounts:profile')
