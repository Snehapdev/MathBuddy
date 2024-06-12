from rest_framework import serializers
from api.models import Equation

class EquationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equation
        fields = ['id','equation', 'type', 'solution', 'user']
