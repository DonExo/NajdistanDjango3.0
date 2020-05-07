from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from configdata import FORBIDDEN_MESAGE

from .forms import UserSearchProfileForm
from .models import SearchProfiles


@login_required()
def search_profile_create(request):
    if request.method == 'POST':
        form = UserSearchProfileForm(request.POST, user=request.user)
        if form.is_valid():
            sp = form.save(commit=False)
            sp.user = request.user
            sp.save()
            messages.info(request, _("Search Profile added!"))
            return redirect(reverse('accounts:profile'))

    form = UserSearchProfileForm(user=request.user)

    context = {
        'title': "Search Profile",
        'form': form,
        'reached_max_sp': request.user.has_search_profile()
    }
    return render(request, 'sp/sp_create.html', context)

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

    if request.method == 'POST':
        form = UserSearchProfileForm(request.POST, instance=search_profile, user=request.user, update=True)
        if form.is_valid():
            form.save()
            messages.info(request, _("Search Profile updated!"))
            return redirect(reverse('accounts:profile'))
        else:
            return render(request, 'sp/sp_update.html', {'form': form})

    form = UserSearchProfileForm(user=request.user, instance=search_profile, update=True)

    context = {
        'title': 'Update Search Profile',
        'form': form
    }
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