"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import logout
from django.conf import settings
import shouter.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('wall/', shouter.views.wall, name = 'wall'),
    path('', shouter.views.login, name='login'),
    path('register/', shouter.views.register, name='register'),
    path('profile/', shouter.views.profile, name='profile'),
    path('ajax/like/', shouter.views.like, name='ajax-like'),
    path('ajax/unlike/', shouter.views.unlike, name='ajax-unlike'),
    path('ajax/invite/', shouter.views.invite, name='ajax-invite'),
    path('dodaj/', shouter.views.dodaj, name='dodaj'),
    path('pokaz/', shouter.views.pokaz, name='pokaz'),
]
