from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserUpdateForm
from .models import User


@login_required
def profile(request):
    context = {
        'title': 'Profile',
        'user': request.user,
        'listings': request.user.get_listings(),
        'search_profiles': request.user.get_search_profiles(),
    }
    return render(request, 'users/profile.html', context)


@login_required
def properties(request):
    context = {
        'title': 'My Properties',
        'listings': request.user.get_listings(),
    }
    return render(request, 'users/properties.html', context)


@login_required
def update(request):
    context = {'title': 'Profile update'}
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
