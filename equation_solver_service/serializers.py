from rest_framework import serializers

from .models import Equation


class EquationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equation
        fields = '__all__'