from rest_framework import serializers
from equation_solver_service.api.models import Equation

class EquationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equation
        fields = ['equation', 'solution']
