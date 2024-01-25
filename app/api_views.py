from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *
from rest_framework import status
from django.db.models import Q,Prefetch


@api_view(['GET'])
def equipos_list(request):
    
    equipos = Equipos.objects.all()
    serializer = EquipoSerializer(equipos, many=True)
    return Response(serializer.data)



@api_view(['GET'])
def equipo_buscar(request):
    if(request.user.has_perm("biblioteca.view_equipo")):
        formulario = BusquedaEquipoForm(request.query_params)
        if(formulario.is_valid()):
            texto = formulario.data.get('textoBusqueda')
            equipos = Equipos.objects.select_related('deporte').prefetch_related('usurio')
            equipos = equipos.filter(Q(nombre__contains=texto) | Q(descripcion__contains=texto)).all()
            serializer = EquipoSerializer(equipos, many=True)
            return Response(serializer.data)
        else:
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"Sin permisos"}, status=status.HTTP_400_BAD_REQUEST)


