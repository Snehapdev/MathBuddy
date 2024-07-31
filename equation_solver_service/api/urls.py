"""
URL configuration for mathbuddy project.

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
from django.contrib import admin
from django.urls import path
from api.views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions



schema_view = get_schema_view(
   openapi.Info(
      title="Equation Solver API",
      default_version='v1',
      description="",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="help@mathbuddy.com")
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
	path("equations/fetch/", fetch_equations),
	path("equations/save/", save_equations),
	path("equations/solve/", solve_equations),
    path('equations/fetch/<int:equation_id>/', fetch_equation_by_id),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('equations/solution-steps/<str:equation>/', get_equation_solution_steps, name='get_equation_solution_steps'),
    path('equations/detect-type/', detect_equation_type, name='detect_equation_type'),
    path('equations/generate_graph/', generate_graph, name='generate_graph'),

]