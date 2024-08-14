from api.models import Equation
from rest_framework.response import Response

from rest_framework.decorators import api_view
import json
from django.http import JsonResponse
from services.equation_solver import solve_trigonometric_equation, solve_equation_with_imaginary_unit, solve_linear_equations, solve_arithmetic_equation, sense_math_equation
from services.steps_generator import get_solution_steps
from services.graph_generator import plot_linear, plot_trigonometric, plot_complex
from django.views.decorators.csrf import csrf_exempt


import logging
from django.urls import path
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi
from api.serializers import EquationSerializer
import io
import base64
import sympy as sp


# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


@swagger_auto_schema(method='get', manual_parameters=[
    openapi.Parameter('user_id', openapi.IN_QUERY, description="User ID", type=openapi.TYPE_STRING),
])
@api_view(http_method_names=["GET"])
def fetch_equations(request):
    user_id = request.query_params.get('user_id') 
    if not user_id:
        return Response({"error": "user_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

    equations = Equation.objects.filter(user_id=user_id)
    serializer = EquationSerializer(equations, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def fetch_equation_by_id(request, equation_id):
    try:
        equation = Equation.objects.get(id=equation_id)
    except Equation.DoesNotExist:
        return Response({"error": "Equation not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = EquationSerializer(equation)
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
            solution = solve_linear_equations(equation)
        elif equation_type == 'trigonometric':
            solution = solve_trigonometric_equation(equation)
        elif equation_type == 'complex':
            solution = solve_equation_with_imaginary_unit(equation)
        else:
            return JsonResponse({'error': 'Invalid equation type.'}, status=400)
    except Exception as e:
        logger.error("Missing required parameters.", e)
        return JsonResponse({'error': str(e)}, status=400)
    
    result = {"equation": equation, "type": equation_type, "solution": solution}
    print(solution)
    print(type(solution))
    print(result["solution"])
    return JsonResponse({'message': 'Equation solved successfully', 'data': result}, status=status.HTTP_200_OK)



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

@api_view(["GET"])
def get_equation_solution_steps(request, equation):
    if not equation:
        return JsonResponse({'error': 'Missing required parameter: equation.'}, status=400)

    try:
        steps = get_solution_steps(equation)
    except Exception as e:
        logger.error("Error in generating solution steps.", exc_info=e)
        return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'equation': equation, 'solution_steps': steps}, status=200)

@csrf_exempt
def detect_equation_type(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        equation = data.get('equation', '')
        print (equation)
        equation_type = sense_math_equation(equation)  # Implement this function
        print(equation_type)
        return JsonResponse({'type': equation_type})
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def generate_graph(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        equation = data.get('equation')
        equation_type = data.get('type')

        if not equation or not equation_type:
            return JsonResponse({'error': 'Invalid input'}, status=400)

        try:
            if equation_type == 'linear':
                image_base64 = plot_linear(equation)
            elif equation_type == 'arithmetic':
                return JsonResponse({'error': 'Graph not supported for arithemetic equations'}, status=400)
            elif equation_type == 'trigonometric':
                image_base64 = plot_trigonometric(equation)
            elif equation_type == 'complex':
                image_base64 = plot_complex(equation)
            else:
                return JsonResponse({'error': 'Unsupported equation type'}, status=400)
            
            return JsonResponse({'image': image_base64})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)