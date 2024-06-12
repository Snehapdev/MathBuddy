from rest_framework import serializers
from api.models import Equation

class EquationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equation
        fields = ['equation', 'type', 'solution', 'user']
