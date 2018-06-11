from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as login_to_session
from django.contrib.auth.models import User
from .forms import RegistrationForm
import requests, json
from slugify import slugify

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
        username = slugify(request.POST['username'])
        user = authenticate(username=username, password=request.POST['password'])
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=username, password=request.POST['password'])
            login_to_session(request, user)

            payload = {'name' : username, 'mail' : request.POST['mail']}
            h = {"Content-Type" : "application/json"}
            r = requests.put('http://users:80/user/' + username, data = json.dumps(payload), headers = h)
            return redirect('wall')

    return render(request, 'register.html', locals())

def wall(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Najpierw sie zaloguj")

    wall = True
    url = 'http://messages:80/messages/' + request.user.username
    r = requests.get(url)
    messages = r.json()
    return render(request, 'wall.html', locals())

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Najpierw sie zaloguj")

    profile = True
    url = 'http://users:80/user/' + request.user.username
    r = requests.get(url)
    info = r.text
    return render(request, 'profile.html', locals())

def dodaj(request):
    j = {'name' : 'john', 'mail' : 'john'}
    s = json.dumps(j)
    print(s)
    h = {"Content-Type" : "application/json"}
    r = requests.put('http://users:80/user/john', data = s, headers = h)
    print(r.url)
    print(r.text)

    return HttpResponse(r.text)

def pokaz(request):
    h = {"Content-Type" : "application/json"}
    r = requests.get('http://users:80/user/john')
    print(r.url)
    # print(r.json())

    return HttpResponse(r.text)
