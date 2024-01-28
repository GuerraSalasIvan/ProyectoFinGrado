from .models import *
from .serializers import *
from rest_framework import serializers


class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipos
        fields = '__all__'
        
        
class DeporteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Deportes
        fields = '__all__'
        
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model=Usuarios
        fields = '__all__'     
    
class EquipoSerializer(serializers.ModelSerializer):
    
    deporte=DeporteSerializer()
    
    usuario = UsuarioSerializer(read_only= True, many=True)
    
    class Meta:
        model = Equipos
        fields = ('nombre','capacidad','deporte','usuario')
        
        
class UbicacionSerializer(serializers.ModelSerializer):
    
    deporte=DeporteSerializer(read_only= True, many=True)
    
    equipo = EquipoSerializer(read_only= True, many=True)
    
    class Meta:
        model = Ubicacion
        fields = ('nombre','capacidad','calle','deporte','equipo')