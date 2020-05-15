import imghdr # internal python library for checking image type

from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django_filters.views import FilterView

from .models import Listing, Image
from .forms import ListingCreateForm, ListingUpdateForm
from .filters import ListingFilter
from configdata import FORBIDDEN_MESAGE, PAGINATOR_ITEMS_PER_PAGE


class ListingIndexView(FilterView):
    template_name = 'listings/list.html'
    filterset_class = ListingFilter

    # TODO: Check why it has slow database connection on this view

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Listings'
        context['latest_5'] = Listing.objects.all().order_by('-created_at')[:5]  # .approved()
        return context

class ListingSearchView(FilterView):
    queryset = Listing.objects.all()  # .approved()
    template_name = 'listings/search.html'
    context_object_name = 'objects'
    paginate_by = PAGINATOR_ITEMS_PER_PAGE
    filterset_class = ListingFilter

    def get_queryset(self):
        return self.queryset.prefetch_related('user', 'city')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Search Listings'
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Listing'
        context['generate_dummy_listing'] = settings.GENERATE_DUMMY_LISTING
        return context


class ListingDetailView(generic.DetailView):
    model = Listing
    template_name = 'listings/detail.html'
    queryset = Listing.objects.select_related('user')

    def get_object(self, queryset=None):
        object = super().get_object()
        object.increment_visited_counter()
        return object

    def post(self, request, *args, **kwargs):
        """
        Custom logic for validating and processing images.
        If the user has uploaded at least one valid file (image) - it is processed and attached it to the listing.
        If there are no valid images in the uploaded files - they are all rejected.
        If all of them are valid - all are attached to the listing.
        The user is informed in any case of the current situation.
        """
        invalid_files = []
        valid_files = []
        image_objects = []
        for file in request.FILES.getlist('images'):
            if imghdr.what(file) == None: # if file is not an image
                invalid_files.append(file)
            else:
                valid_files.append(file)

        if len(valid_files) == 0:
            messages.error(request, "There were no valid file images to be uploaded")
            return redirect(request.get_raw_uri())
        elif len(valid_files) > 0 and len(invalid_files) > 0:
            messages.error(request, f"Some of the files have been in invalid format or damaged. We've managed to upload only {len(valid_files)} files.")
        else:
            messages.error(request, f"Successfully uploaded {len(valid_files)} images!")

        for image in valid_files:
            object = Image(
                listing=self.get_object(),
                image=image
            )
            image_objects.append(object)
        Image.objects.bulk_create(image_objects)
        return redirect(request.get_raw_uri())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listing details'
        context['prev_page'] = self.request.META.get('HTTP_REFERER', None)
        return context


class ListingUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Listing
    template_name = 'listings/update.html'
    form_class = ListingUpdateForm
    permission_denied_message = FORBIDDEN_MESAGE

    def get_success_url(self):
        messages.success(self.request, _("You've successfully updated the property!"))
        return reverse_lazy('accounts:properties')

    def form_valid(self, form):
        return super().form_valid(form)

    # Checks if the listing owner is different than the request user
    def test_func(self):
        return self.request.user == self.get_object().user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Listing'
        return context


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
