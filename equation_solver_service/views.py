from django.shortcuts import render
from equation_solver_service.models import Equation
#from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework.views import APIView
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse
from equation_solver_service.services.equation_solver import solve_arithmetic_equation
from equation_solver_service.services.equation_solver import solve_linear_equation
from equation_solver_service.services.equation_solver import solve_trigonometric_equation



from equation_solver_service.serializers import EquationSerializer


# Create your views here.

@api_view(http_method_names=["GET"])
def fetch_equations(request):
    equations = Equation.objects.all()
    serializer = EquationSerializer(equations, many=True)
    return Response(serializer.data)

@api_view(http_method_names=["POST"])
def solve_equations(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    equation_type = data.get('type')
    equation = data.get('equation')

    if not equation_type or not equation:
        return JsonResponse({'error': 'Missing required parameters.'}, status=400)

    try:
        if equation_type == 'arithmetic':
            solution = solve_arithmetic_equation(equation)
        elif equation_type == 'linear':
            solution = solve_linear_equation(equation)
        elif equation_type == 'trigonometric':
            solution = solve_trigonometric_equation(equation)
        else:
            return JsonResponse({'error': 'Invalid equation type.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'equation': equation, 'solution': solution})

@api_view(http_method_names=["POST"])
def save_equations(request):
    pass


    