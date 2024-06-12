
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from django import forms

from django.forms.widgets import PasswordInput, TextInput

from django.core.exceptions import ValidationError
import os


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

class UploadImageForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
        'class': 'form-control',
        'placeholder': 'Choose an image file'
    }))

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            raise ValidationError("No image uploaded!")

        max_size = 2 * 1024 * 1024 
        if image.size > max_size:
            raise ValidationError(f"The image is too large. The maximum file size is {max_size / (1024 * 1024)} MB")

        valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
        extension = os.path.splitext(image.name)[1].lower()
        if extension not in valid_extensions:
            raise ValidationError("Unsupported file format. Supported formats: jpg, jpeg, png, gif")

        return image