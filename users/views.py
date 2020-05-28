from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserUpdateForm
from .models import User


@login_required
def profile(request):
    context = {
        'title': 'My Profile',
        'user': request.user,
        'listings': request.user.get_listings(),
        'search_profiles': request.user.get_search_profiles(),
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
    }
    return render(request, 'users/properties.html', context)


@login_required
def bookmarks(request):
    context = {
        'title': 'Bookmarked Properties',
        'bookmarks': request.user.get_bookmarks(),
    }
    return render(request, 'users/bookmarks.html', context)


@login_required
def update(request):
    context = {'title': 'Update Profile'}
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


def user_identifier(request, identifier):
    try:
        user = User.objects.prefetch_related('listings__city').get(identifier=identifier)
    except User.DoesNotExist:
        raise Http404("User does not exist.")
    if user == request.user:
        messages.info(request, "You have been redirected to your own profile.")
        return redirect(reverse('accounts:profile'))

    context = {
        'title': 'User profile',
        'user': user,
        'listings': user.get_listings()
    }
    return render(request, 'users/user.html', context)


@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.deactivate()
        logout(request)
        messages.info(request, "Your account has been disabled! We are sorry to see you go.")
        return redirect(reverse('index'))
    return render(request, 'users/delete.html')
