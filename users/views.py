from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .forms import UserUpdateProfileForm
from .models import User


def index(request):
    # return HttpResponse("Hello world!")
    return render(request, 'users/index.html', {'foo': 'bar'})


@login_required
def profile(request):
    # if request.method == 'POST':
    # @TODO: Add ability to edit Profile image

    listings = request.user.get_listings()

    context = {}
    context.update({
        'user': request.user,
        'title': "Profile be",
        'listings': listings
    })

    return render(request, 'users/profile.html', context)


# @TODO: Make this nice!
@login_required()
def update(request):
    instance = get_object_or_404(User, id=request.user.id)
    form = UserUpdateProfileForm(instance=instance)

    if request.method == 'POST':
        form = UserUpdateProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))

    context = {'title': "Update profile"}
    context['form'] = form

    return render(request, 'users/update.html', context)