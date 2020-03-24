from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    # return HttpResponse("Hello world!")
    return render(request, 'users/index.html', {'foo': 'bar'})



def profile(request):
    # if request.method == 'POST':

    context = {}
    context.update({
        'user': request.user,
        'title': "Profile be"
    })

    return render(request, 'users/profile.html', context)