from .models import *
from .serializers import *
from rest_framework import serializers


class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipos
        fields = '__all__'