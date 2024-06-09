
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput


# - Create/Register a user (Model Form)

class CreateUserForm(UserCreationForm):
    username = forms.CharField(widget=TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control'
    }))
    email = forms.EmailField(widget=TextInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control'
    }))
    password1 = forms.CharField(label="Password", widget=PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control'
    }))
    password2 = forms.CharField(label="Confirm Password", widget=PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control'
    }))
    password = forms.CharField(widget=PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control'
    }))
