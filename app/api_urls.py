from django.urls import path
from .api_views import *

urlpatterns = [
    path('equipos',equipos_list),
    path('busqueda/equipo_simple', equipo_buscar),
    path('equipos/busqueda_avanzada', equipos_busqueda_avanzada)
]