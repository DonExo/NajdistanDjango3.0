from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from configdata import FORBIDDEN_MESAGE
from .forms import UserSearchProfileForm
from .models import SearchProfiles


@login_required()
def search_profile_manage(request):
    context = {'title': "Manage Search Profiles"}
    context.update({'reached_max_sp': request.user.has_search_profile(),
                    'search_profiles': request.user.get_search_profiles(),
                    'active_sp': request.user.get_search_profiles().count_active(),
                    'crumbs': {
                        "Home": reverse('index'),
                        "Account": reverse('accounts:profile'),
                        "Search Profile": '#',
                    }
                    })
    return render(request, 'searchprofile/manage.html', context)


@login_required()
def search_profile_create(request):
    context = {
        'title': "Create Search Profile",
        'crumbs': {
           "Home": reverse('index'),
           "Account": reverse('accounts:profile'),
           "Search Profile": reverse('searchprofiles:manage'),
           "Create": "#"
        }
    }

    if request.method == 'POST':
        form = UserSearchProfileForm(request.POST, user=request.user)
        context.update({'form': form})
        if form.is_valid():
            sp = form.save(commit=False)
            sp.user = request.user
            sp.save()
            messages.success(request, _("Search Profile added!"))
            return redirect(reverse('searchprofiles:manage'))
        else:
            return render(request, 'searchprofile/create.html', context)

    form = UserSearchProfileForm(user=request.user)

    context.update({'form': form, 'reached_max_sp': request.user.has_search_profile()})
    return render(request, 'searchprofile/create.html', context)


@login_required()
def search_profile_delete(request, pk):
    search_profile = get_object_or_404(SearchProfiles, pk=pk)
    if search_profile.user != request.user:
        return HttpResponseForbidden(_(FORBIDDEN_MESAGE))
    search_profile.delete()
    messages.info(request, _("Search Profile deleted."))
    return redirect(reverse('searchprofiles:manage'))


@login_required()
def search_profile_update(request, pk):
    search_profile = get_object_or_404(SearchProfiles, pk=pk)
    if search_profile.user != request.user:
        return HttpResponseForbidden(_(FORBIDDEN_MESAGE))

    context = {
        'title': _('Update Search Profile'),
        'crumbs': {
            "Home": reverse('index'),
            "Account": reverse('accounts:profile'),
            "Search Profile": reverse('searchprofiles:manage'),
            "Update": "#"
        }
    }

    if request.method == 'POST':
        form = UserSearchProfileForm(request.POST, instance=search_profile, user=request.user, update=True)
        context.update({'form': form})
        if form.is_valid():
            if form.has_changed():
                form.save()
                messages.info(request, _("Search Profile updated!"))
            return redirect(reverse('searchprofiles:manage'))
        else:
            return render(request, 'searchprofile/update.html', context)

    form = UserSearchProfileForm(user=request.user, instance=search_profile, update=True)
    context.update({'form': form})
    return render(request, 'searchprofile/update.html', context)


# TODO: Use the ajax_required decorator once 'compare view' is merged
@require_http_methods(['POST'])
@csrf_exempt
def search_profile_toggle(request):
    # Sanity checks
    if not request.is_ajax():
        return JsonResponse({'error': 'Non-Ajax request detected'}, status=403)
    # if not request.method == 'POST':
    #     return JsonResponse({'error': 'This request has to be done via POST.'}, status=403)
    ajax_user = getattr(request, 'user', None)
    if ajax_user.is_anonymous:
        return JsonResponse({'error': 'You need to be logged-in for this action'}, status=403)
    sp_key = request.POST.get('sp_pk', None)
    if not sp_key:
        return JsonResponse({'error': 'Requested key not found in POST.'}, status=403)
    try:
        search_profile = SearchProfiles.objects.get(pk=sp_key)
    except SearchProfiles.DoesNotExist:
        return JsonResponse({'error': 'Requested Search Profile not found.'}, status=404)
    if search_profile.user != ajax_user:
        return JsonResponse({'error': "You don't have permission to do this action."}, status=403)

    search_profile.is_active = not search_profile.is_active
    search_profile.save()
    return JsonResponse({'data': 'Search Profile successfully updated!'}, status=200)
