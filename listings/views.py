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
    queryset = Listing.objects.all()
    template_name = 'listings/list.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return self.queryset.all()  # for testing purposes
        # return self.queryset.filter(is_approved=True)

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


    # @transaction.atomic
    # def post(self, request, *args, **kwargs):
    #
    #
    #     # for file in request.FILES.getlist('images'):
    #     #     instance = Image.objects.create(
    #     #         listing=Listing.objects.first(),
    #     #         image=file
    #     #     )
    #     #     print(file)
    #     #     # @TODO: Handle listing images upload logic
    #     #     # fs = FileSystemStorage()
    #         # filename = fs.save(file.name, file)
    #         # uploaded_file_url = fs.url(filename)
    #     return super().post(request, *args, **kwargs)


class ListingDetailView(generic.DetailView):
    model = Listing
    template_name = 'listings/detail.html'


class ListingUpdateView(UserPassesTestMixin, generic.UpdateView):
    model = Listing
    template_name = 'listings/update.html'
    form_class = ListingUpdateForm
    permission_denied_message = FORBIDDEN_MESAGE

    def get_success_url(self):
        return reverse_lazy('listings:detail', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        return super().form_valid(form)
        # return redirect(reverse_lazy('list'))

    # Check if the listing user is == to the request user trying to delete it
    def test_func(self):
        return self.request.user == self.get_object().user


# class ListingDeleteView(View):
#     def get_object(self):


def delete_listing(request, slug):
    listing = get_object_or_404(Listing, slug=slug)
    if listing.user != request.user:
        return HttpResponseForbidden(FORBIDDEN_MESAGE)
    listing.delete()
    messages.info(request, "Deleted listing!")
    return redirect(reverse('accounts:profile'))

