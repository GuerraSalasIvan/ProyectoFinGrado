from django.urls import path
from .api_views import *

urlpatterns = [
    path('equipos',equipos_list),
    path('busqueda/equipo_simple', equipo_buscar),
]