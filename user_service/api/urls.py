"""
URL configuration for user_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# user_service/urls.py

from django.urls import path
from .views import homepage, login, register, dashboard, logout, fetch_user_equations
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated



schema_view = get_schema_view(
   openapi.Info(
      title="User Service API",
      default_version='v1',
      description="",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="help@mathbuddy.com")
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('users/', homepage, name='homepage'),
    path('users/register/',  register, name='register'),
    path('users/login/', login, name='login'),
    path('users/dashboard/', dashboard, name="dashboard"),
    path('users/logout/', logout, name="logout"),
    path('fetch_user_equations/', fetch_user_equations, name='fetch_user_equations'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

