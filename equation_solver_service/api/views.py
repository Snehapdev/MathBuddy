from equation_solver_service.api.models import Equation
from rest_framework.response import Response

from rest_framework.decorators import api_view
import json
from django.http import JsonResponse
from equation_solver_service.services.equation_solver import solve_arithmetic_equation
from equation_solver_service.services.equation_solver import solve_linear_equation
from equation_solver_service.services.equation_solver import solve_trigonometric_equation
import logging
from django.urls import path
from drf_yasg.utils import swagger_auto_schema



from equation_solver_service.api.serializers import EquationSerializer


# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)



# Create your views here.
@api_view(http_method_names=["GET"])
def fetch_equations(request):
    equations = Equation.objects.all()
    serializer = EquationSerializer(equations, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='post', request_body=EquationSerializer)
@api_view(http_method_names=["POST"])
def solve_equations(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)

    equation_type = data.get('type')
    equation = data.get('equation')

    if not equation_type or not equation:
        logger.error("Missing required parameters.")
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
        logger.error("Missing required parameters.", e)
        return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'equation': equation, 'solution': solution})

@swagger_auto_schema(method='post', request_body=EquationSerializer)
@api_view(http_method_names=["POST"])
def save_equations(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON.'}, status=400)
    
    serializer = EquationSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Equation saved successfully"}, status=201)
    else:
        return JsonResponse(serializer.errors, status=400)