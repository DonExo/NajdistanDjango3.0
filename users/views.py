from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserUpdateForm
from .models import User
from .tasks import send_deactivation_email


@login_required
def profile(request):
    context = {
        'title': 'My Profile',
        'user': request.user,
        'listings': request.user.get_listings(),
        'search_profiles': request.user.get_search_profiles(),
        'crumbs': {
            "Home": reverse('index'),
            "Account": '#',
        }
    }
    return render(request, 'users/profile.html', context)


@login_required
def properties(request):
    user_listings = request.user.get_listings()
    context = {
        'title': 'My Properties',
        'active': user_listings.active(),
        'inactive': user_listings.inactive(),
        'pending': user_listings.pending(),
        'has_listings': request.user.has_listings(),
        'crumbs': {
            "Home": reverse('index'),
            "Account": reverse('accounts:profile'),
            "Properties": '#',
        }
    }
    return render(request, 'users/properties.html', context)


@login_required
def bookmarks(request):
    context = {
        'title': 'Bookmarked Properties',
        'bookmarks': request.user.get_bookmarks(),
        'crumbs': {
            "Home": reverse('index'),
            "Account": reverse('accounts:profile'),
            "Bookmarked": '#',
        }
    }
    return render(request, 'users/bookmarks.html', context)


@login_required
def update(request):
    context = {'title': 'Update Profile',
               'crumbs': {
                   "Home": reverse('index'),
                   "Account": reverse('accounts:profile'),
                   "Update": "#"
               }
           }

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        context.update({'form': form})
        if form.changed_data and form.is_valid():
            form.save()
            messages.info(request, "Account updated successfully!")
        else:
            return render(request, 'users/update.html', context)
        return redirect(reverse('accounts:profile'))
    form = UserUpdateForm(instance=request.user)
    context.update({'form': form})
    return render(request, 'users/update.html', context)


def publisher(request, identifier):
    try:
        user = User.objects.prefetch_related('listings__city').get(identifier=identifier)
    except User.DoesNotExist:
        raise Http404("User does not exist.")
    if user == request.user:
        messages.info(request, "You have been redirected to your own profile.")
        return redirect(reverse('accounts:profile'))

    context = {
        'title': 'Publisher',
        'publisher': user,
        'listings': user.get_listings(),
        'crumbs': {
            "Home": reverse('index'),
            "Publisher": '#',
        }

    }
    return render(request, 'users/publisher.html', context)


@login_required
def deactivate_account(request):
    context = {
        'title': 'Deactivate Account',
           'crumbs': {
               "Home": reverse('index'),
               "Account": reverse('accounts:profile'),
               "Deactivate": "#"
           }
       }
    if request.method == 'POST':
        request.user.deactivate()
        logout(request)
        send_deactivation_email.delay(request.user.pk)
        messages.info(request, "Your account has been disabled! We are sorry to see you go.")
        return redirect(reverse('index'))
    return render(request, 'users/deactivate.html', context)
