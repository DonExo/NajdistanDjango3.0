from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import UserUpdateProfileForm
from .models import User


def index(request):
    return render(request, 'users/index.html', {'foo': 'bar'})


@login_required
def profile(request):
    listings = request.user.get_listings()
    context = {}
    context.update({
        'user': request.user,
        'title': "Profile be",
        'listings': listings
    })
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
