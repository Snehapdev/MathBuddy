from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from . forms import CreateUserForm, LoginForm, UploadImageForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import requests



User = get_user_model()


@api_view(http_method_names=["GET"])
@permission_classes([permissions.AllowAny]) 
def homepage(request):
     return render(request, 'user_service/index.html')


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    context = {'registerform':form}
    return render(request, 'user_service/register.html', context=context)



def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("dashboard")

    context = {'loginform':form}
    return render(request, 'user_service/login.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect("homepage")


@login_required(login_url="login")
def dashboard(request):
    form = UploadImageForm()
    return render(request, 'user_service/dashboard.html',{'upload_form': form})

@login_required
def fetch_user_equations(request):
    # Access the logged-in user's ID
    user_id = request.user.id
    # URL of the equation service
    equation_service_url = 'http://localhost:8000/equations/fetch/'
    
    try:
        # Make a request to the equation service with the user ID as a parameter
        response = requests.get(equation_service_url, params={'user_id': user_id})
        response.raise_for_status()
        equations = response.json()
    except requests.RequestException as e:
        print(f"Error fetching equations: {e}")
        equations = []

    # Render a template with the fetched equations
    return render(request, 'user_service/user_equations.html', {'equations': equations})