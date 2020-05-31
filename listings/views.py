from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django_filters.views import FilterView

from .filters import ListingFilter
from .forms import ListingCreateForm, ListingUpdateForm
from .models import Listing, Image
from .utils import _check_image_validness
from configdata import FORBIDDEN_MESAGE, PAGINATOR_ITEMS_PER_PAGE


class ListingIndexView(FilterView):
    template_name = 'listings/index.html'
    filterset_class = ListingFilter

    # TODO: Check why it has slow database connection on this view
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        # Make this FEATURED properties
        context['latest_5'] = Listing.objects.all().order_by('-created_at')[:5]  # .approved() / featured()
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
    model = Listing
    login_url = reverse_lazy('auth_login')
    template_name = 'listings/create.html'
    form_class = ListingCreateForm
    success_message = "Property successfully created!"

    def get_success_url(self):
        # dummy_task.delay(self.object.slug)
        return reverse_lazy('listings:detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        # Assign the request user to the Listing object
        listing = form.save(commit=False)
        listing.user = self.request.user
        listing.save()

        # Check the uploaded files
        files = self.request.FILES.getlist('images')
        if files:
            valid_images, invalid_files = _check_image_validness(files)
            if valid_images:
                image_objects = []
                for image in valid_images:
                    obj = Image(listing=listing, image=image)
                    image_objects.append(obj)
                Image.objects.bulk_create(image_objects)
            if invalid_files:
                messages.error(self.request,
                               _(f"You have submitted {len(invalid_files)} invalid files that have been rejected."))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Submit Property'
        context['generate_dummy_listing'] = settings.GENERATE_DUMMY_LISTING
        return context


class ListingDetailView(generic.DetailView):
    model = Listing
    template_name = 'listings/detail.html'
    queryset = Listing.objects.select_related('user')

    def get(self, request, *args, **kwargs):
        listing = self.get_object()
        listing.increment_visited_counter()  # TODO: Make this async
        if not listing.is_available and request.user != listing.user:
            messages.warning(self.request, "You can not access this property. The owner has marked it as un-available!")
            return redirect(reverse('listings:search'))
        return super().get(request, *args, **kwargs)

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
        return reverse_lazy('accounts:properties')

    def form_valid(self, form):
        files = self.request.FILES.getlist('images')
        # Check the uploaded files
        if files:
            valid_images, invalid_files = _check_image_validness(files)
            if valid_images:
                image_objects = []
                for image in valid_images:
                    obj = Image(listing=self.get_object(), image=image)
                    image_objects.append(obj)
                Image.objects.bulk_create(image_objects)
                messages.success(self.request, _(f"You have added {len(image_objects)} new image(s) to your property!"))
            if invalid_files:
                messages.error(self.request,
                               _(f"You have submitted {len(invalid_files)} invalid files that have been rejected."))
        if form.has_changed():
            messages.success(self.request, _("You've successfully updated the property!"))
        return super().form_valid(form)

    # Checks if the listing owner is different than the request user
    def test_func(self):
        return self.request.user == self.get_object().user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Listing'
        context['prev_page'] = self.request.META.get('HTTP_REFERER', None)
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
        return reverse('accounts:properties')


class ListingCompareView(generic.ListView):
    template_name = 'listings/compare.html'

    def get_queryset(self):
        property_slugs = self.request.GET.getlist('c', None)
        if property_slugs:
            listings = Listing.objects.filter(slug__in=property_slugs)
            return listings
        return None
