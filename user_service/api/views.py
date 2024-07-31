from django.shortcuts import render
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from . forms import CreateUserForm, LoginForm, UploadImageForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
import requests
import base64
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import google.generativeai as genai
from django.contrib import messages




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
        print(form.is_valid())
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                auth_login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Error in data. Please check your input.")

    context = {'loginform': form}
    return render(request, 'user_service/login.html', context)



def logout(request):
    auth.logout(request)
    return redirect("homepage")


@login_required(login_url="login")
def dashboard(request):
    if request.method == 'POST':
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']

            # Save the uploaded image to the default storage
            image_path = default_storage.save(f'uploads/{image.name}', ContentFile(image.read()))

            # Read the image file into memory
            content = default_storage.open(image_path).read()

            # Base64 encode the image content
            encoded_image = base64.b64encode(content).decode('utf-8')

            # Your API key (ensure this is securely stored, e.g., in environment variables or Django settings)
            api_key = settings.GOOGLE_VISION_API_KEY

            # Vision API endpoint
            url = f'https://vision.googleapis.com/v1/images:annotate?key={api_key}'

            # Prepare the request payload
            payload = {
                'requests': [
                    {
                        'image': {
                            'content': encoded_image
                        },
                        'features': [
                            {
                                'type': 'DOCUMENT_TEXT_DETECTION'
                            }
                        ]
                    }
                ]
            }

            # Make the request to the Vision API
            response = requests.post(url, json=payload)
            result = response.json()

            # Extract text from the response
            try:
                handwritten_text = result['responses'][0]['fullTextAnnotation']['text'].lower()
            except KeyError:
                handwritten_text = ""

            # Get the type of the equation
            equation_type = sense_math_equation(handwritten_text)

            context = {
                'upload_form': form,
                'handwritten_text': handwritten_text,
                'encoded_image': encoded_image,
                'equation_type': equation_type
            }
            return render(request, 'user_service/dashboard.html', context=context)
        else:
            # Handle invalid form data, perhaps by re-rendering the form with error messages
            print(form.errors)  # Print errors to debug console
    else:
        form = UploadImageForm()

    return render(request, 'user_service/dashboard.html', {'upload_form': form})

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

# Function to sense the type of mathematical equation
def sense_math_equation(equation):
    # Configure your API key
    genai.configure(api_key=settings.GEN_LANGUAGE_API_KEY)
    # Choose a model that's appropriate for your use case
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Create the prompt with the equation
    prompt = f"Classify the following mathematical equation as one of the following types: linear, trigonometric, arithmetic, or complex. Only respond with the type. Equation: {equation}"
    response = model.generate_content(prompt)

    # List of valid types
    valid_types = {'linear', 'trigonometric', 'arithmetic', 'complex'}
    
    # Extract the response text and filter it
    if response:
        response_text = response.text.strip().lower()
        # Return the first valid type found in the response
        for valid_type in valid_types:
            if valid_type in response_text:
                return valid_type
    return "Error"
