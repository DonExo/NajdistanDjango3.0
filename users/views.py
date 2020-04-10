from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserUpdateProfileForm, UserSearchProfileForm
from .models import User


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
    form = UserUpdateProfileForm(instance=request.user)
    if request.method == 'POST':
        form = UserUpdateProfileForm(request.POST, request.FILES, instance=request.user)
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
            messages.info(request, "Search Profile form added!")
            return redirect(reverse('accounts:profile'))

    return render(request, 'users/search_profile.html', {'form': form})
