from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *


@api_view(['GET'])
def equipos_list(request):
    
    equipos = Equipos.objects.all()
    serializer = EquipoSerializer(equipos, many=True)
    return Response(serializer.data)

