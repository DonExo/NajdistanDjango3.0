from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .forms import UserUpdateForm, UserSearchProfileForm
from .models import User, SearchProfiles

from configdata import FORBIDDEN_MESAGE


def index(request):
    return render(request, 'users/index.html', {'foo': 'bar'})


@login_required
def profile(request):
    context = {
        'title': "Profile be",
        'user': request.user,
        'listings': request.user.get_listings(),
        'search_profiles': request.user.get_search_profiles(),
    }
    return render(request, 'users/profile.html', context)


@login_required()
def update(request):
    form = UserUpdateForm(instance=request.user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.info(request, "Account updated successfully!")
            return redirect(reverse('accounts:profile'))
    context = {'title': 'Update profile', 'form': form}
    return render(request, 'users/update.html', context)


def user_identifier(request, identifier):
    try:
        user = User.objects.prefetch_related('listings__city').get(identifier=identifier)
    except User.DoesNotExist:
        raise Http404("User does not exist.")
    if user == request.user:
        messages.info(request, "You have been redirected to your own profile.")
        return redirect(reverse('accounts:profile'))

    context = {
        'user': user,
        'listings': user.get_listings()
    }
    return render(request, 'users/user.html', context)

@login_required()
def search_profile_create(request):
    form = UserSearchProfileForm(user=request.user)

    if request.method == 'POST':
        form = UserSearchProfileForm(request.POST, user=request.user)
        if form.is_valid():
            sp = form.save(commit=False)
            sp.user = request.user
            sp.save()
            messages.info(request, _("Search Profile added!"))
            return redirect(reverse('accounts:profile'))

    return render(request, 'sp/sp_create.html', {
        'form': form,
        'reached_max_sp': request.user.has_search_profile(),
    })

@login_required()
def search_profile_delete(request, pk):
    search_profile = get_object_or_404(SearchProfiles, pk=pk)
    if search_profile.user != request.user:
        return HttpResponseForbidden(_(FORBIDDEN_MESAGE))
    search_profile.delete()
    messages.info(request, _("Search Profile deleted."))
    return redirect(reverse('accounts:profile'))


@login_required()
def search_profile_update(request, pk):
    search_profile = get_object_or_404(SearchProfiles, pk=pk)
    if search_profile.user != request.user:
        return HttpResponseForbidden(_(FORBIDDEN_MESAGE))

    context = {'title': _('Update Search Profile')}
    if request.method == 'POST':
        form = UserSearchProfileForm(request.POST, instance=search_profile, user=request.user, update=True)
        if form.is_valid():
            form.save()
            messages.info(request, _("Search Profile updated!"))
            return redirect(reverse('accounts:profile'))
        else:
            context.update({'form': form})
            return render(request, 'sp/sp_update.html', context)

    form = UserSearchProfileForm(user=request.user, instance=search_profile, update=True)
    context.update({'form': form})
    return render(request, 'sp/sp_update.html', context)


#@TODO: Make this Ajax request with no page refresh
@login_required()
def toggle_sp_status(request, pk):
    search_profile = get_object_or_404(SearchProfiles, pk=pk)
    if search_profile.user != request.user:
        return HttpResponseForbidden(_(FORBIDDEN_MESAGE))
    search_profile.is_active = not search_profile.is_active
    search_profile.save()
    messages.info(request, _("Search Profile Updated."))
    return redirect(reverse('accounts:profile'))