from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login as login_to_session
from django.contrib.auth.models import User
from .forms import RegistrationForm
import requests, json
from slugify import slugify
import pika

# Create your views here.

def get_object_or_empty(json, str):
    if str in json.keys():
        return json[str]
    return []

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

    if request.method == "POST":
        j = {'message' : request.POST['message']}
        s = json.dumps(j)
        h = {"Content-Type" : "application/json"}
        r = requests.put('http://messages:80/messages/' + request.user.username, data = s, headers = h)

    wall = True
    url = 'http://messages:80/messages_for/' + request.user.username
    r = requests.get(url)
    messages = get_object_or_empty(r.json(), 'messages')

    url = 'http://relations:80/sent-invitations/' + request.user.username
    r = requests.get(url)
    invited = get_object_or_empty(r.json(), 'invitations')

    return render(request, 'wall.html', locals())

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Najpierw sie zaloguj")

    profile = True
    url = 'http://users:80/user/' + request.user.username
    r = requests.get(url)
    info = r.json()
    userinfo = [('Username', info['username']),
                ('Email', info['mail']),
                ('Number of published messages', info['messages'])]

    if 'likes' in info.keys():
        userinfo.append(('Number of likes you\'ve received', info['likes']))

    url = 'http://relations:80/sent-invitations/' + request.user.username
    r = requests.get(url)
    invited = get_object_or_empty(r.json(), 'invitations')

    url = 'http://relations:80/received-invitations/' + request.user.username
    r = requests.get(url)
    invitations = get_object_or_empty(r.json(), 'invitations')

    url = 'http://relations:80/relations/' + request.user.username
    r = requests.get(url)
    friends_names = get_object_or_empty(r.json(), 'relations')

    friends_profiles = []
    for name in friends_names:
        url = 'http://users:80/user/' + name
        r = requests.get(url)
        friends_profiles.append(r.json())

    friends = friends_profiles

    return render(request, 'profile.html', locals())

@require_POST
def like(request):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='message-broker'))
    channel = connection.channel()

    channel.exchange_declare(exchange='likes',
                             exchange_type='fanout')

    channel.basic_publish(exchange='likes',
                          routing_key='',
                          body=request.POST['message_id'])
    connection.close()

    url = 'http://messages:80/like/' + request.user.username
    d = json.dumps({"idx" : request.POST['message_id']})
    h = {"Content-Type" : "application/json"}
    r = requests.put(url, data = d, headers = h)

@require_POST
def unlike(request):
    url = 'http://messages:80/like/' + request.user.username
    d = json.dumps({"idx" : request.POST['message_id']})
    h = {"Content-Type" : "application/json"}
    r = requests.delete(url, data = d, headers = h)

@require_POST
def invite(request):
    url = 'http://relations:80/sent-invitations/' + request.user.username
    d = json.dumps({"invited" : request.POST['invited']})
    h = {"Content-Type" : "application/json"}
    r = requests.put(url, data = d, headers = h)

@require_POST
def accept(request):
    url = 'http://relations:80/relations/' + request.user.username
    d = json.dumps({"related_username" : request.POST['invited']})
    h = {"Content-Type" : "application/json"}
    r = requests.put(url, data = d, headers = h)
