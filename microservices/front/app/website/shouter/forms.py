from django import forms
from django.contrib.auth.models import User

def usernameValidator(name):
    if User.objects.filter(username=name).exists():
        raise forms.ValidationError('User with the same username already exists.')

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=64, label='Username', validators=[usernameValidator])
    password = forms.CharField(max_length=64, label='Password', widget=forms.PasswordInput())
