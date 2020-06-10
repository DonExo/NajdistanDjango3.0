from django.conf import settings
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views import generic
from django.http import JsonResponse
from django_filters.views import FilterView

from .decorators import ajax_required
from .filters import ListingFilter
from .forms import ListingCreateForm, ListingUpdateForm
from .models import Listing, Image
from .mixins import CustomLoginRequiredMixin
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
        context['latest_5'] = Listing.objects.active().order_by('-created_at')[:5]  # featured()
        return context


class ListingSearchView(FilterView):
    queryset = Listing.objects.active()
    template_name = 'listings/search.html'
    paginate_by = PAGINATOR_ITEMS_PER_PAGE
    filterset_class = ListingFilter

    def get_queryset(self):
        return self.queryset.prefetch_related('user', 'city')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listings'
        context['crumbs'] = {
            "Home": reverse('index'),
            "Listings": '#',
        }
        return context


class ListingCreateView(CustomLoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Listing
    login_url = reverse_lazy('auth_login')
    template_name = 'listings/create.html'
    form_class = ListingCreateForm
    success_message = "Property successfully created!"

    def get_success_url(self):
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

        # TASKS.check for active SPs with value 'instant' (check MRO of this View)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Submit Property'
        context['generate_dummy_listing'] = settings.GENERATE_DUMMY_LISTING
        context['crumbs'] = {
            "Home": reverse('index'),
            "Listings": reverse('listings:search'),
            "Create": '#',
        }
        return context


class ListingDetailView(generic.DetailView):
    model = Listing
    template_name = 'listings/detail.html'
    queryset = Listing.objects.select_related('user')

    def get(self, request, *args, **kwargs):
        listing = self.get_object()
        if not listing.is_active() and listing.user != request.user:
            messages.warning(self.request, "This property can not be viewed.")
            return redirect(reverse('listings:search'))
        listing.increment_visited_counter(self.request.user)  # TODO: Make this async
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_object().title
        context['prev_page'] = self.request.META.get('HTTP_REFERER', None)
        return context


class ListingUpdateView(CustomLoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
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


class ListingDeleteView(CustomLoginRequiredMixin, UserPassesTestMixin, generic.RedirectView):
    # Checks if the listing owner is different than the request user
    def test_func(self):
        listing = get_object_or_404(Listing, slug=self.kwargs.get('slug'))
        return self.request.user == listing.user

    def get_redirect_url(self, *args, **kwargs):
        listing = get_object_or_404(Listing, slug=self.kwargs.get('slug'))
        listing.delete()
        messages.info(self.request, "Listing deleted.")
        return reverse('accounts:properties')


class ListingToggleStatusView(CustomLoginRequiredMixin, UserPassesTestMixin, generic.RedirectView):
    # Checks if the listing owner is different than the request user
    def test_func(self):
        listing = get_object_or_404(Listing, slug=self.kwargs.get('slug'))
        return self.request.user == listing.user

    def get_redirect_url(self, *args, **kwargs):
        listing = get_object_or_404(Listing, slug=self.kwargs.get('slug'))
        listing.toggle_status()
        messages.success(self.request, "Property status updated successfully!")
        return reverse('accounts:properties')


class ListingCompareView(generic.ListView):
    template_name = 'listings/compare.html'

    def get(self, request, *args, **kwargs):
        if not self.get_queryset() or self.get_queryset().count() < 2:
            messages.error(request, "You need at least to properties for compare.")
            return redirect(reverse('listings:search'))
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        property_slugs = self.request.GET.getlist('c', None)
        if property_slugs:
            listings = Listing.objects.filter(slug__in=property_slugs)
            return listings
        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Compare Properties'
        context['crumbs'] = {
            "Home": reverse('index'),
            "Listings": reverse('listings:search'),
            "Compare": '#'
        }
        return context


class ListingJsonData(generic.View):
    """
    A view that returns json response to the frontend with the neeeded data for the CompareView functionality
    """

    @csrf_exempt
    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        slug_key = request.POST.get('propSlug', None)
        if not slug_key:
            return JsonResponse({'error': 'Requested key not found in POST.'}, status=403)
        try:
            listing = Listing.objects.get(slug=slug_key)
        except Listing.DoesNotExist:
            return JsonResponse({'error': 'Requested Listing not found.'}, status=404)

        json_data = {
            "propSlug": slug_key,
            'propTitle': listing.title,
            'propPrice': listing.price,
            'propHref': listing.get_absolute_url(),
            'propCoverImage': listing.get_cover_image().url,
            'propListingType': listing.listing_type,
            'propHomeType': listing.home_type
        }
        return JsonResponse({'propData': json_data}, status=200)
