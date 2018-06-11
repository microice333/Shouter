from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as login_to_session
from django.contrib.auth.models import User

# Create your views here.

def login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login_to_session(request, user)
            return redirect('wall')
        else:
            error = True;

    return render(request, 'login.html', locals())

def register(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            login_to_session(request, user)
            return redirect('main')

    return render(request, 'register.html', locals())

def wall(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Najpierw sie zaloguj")

    wall = True
    return render(request, 'wall.html', locals())

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Najpierw sie zaloguj")

    profile = True
    return render(request, 'profile.html', locals())
