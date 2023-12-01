from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.indice, name='indice'),
    path('usuarios', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/<str:equipo>', views.usuarios_equipo, name='usuarios_equipo'),
    path('equipos', views.mostar_equipo, name='mostar_equipo'),
    path('lista_deportes', views.lista_deportes, name='lista_deportes'),
    path('usuarios_mayores/<int:edad>', views.usuarios_mayores, name='usuarios_mayores'),
    path('ubicacion_cubierta/<str:deporte>', views.ubicacion_cubierta_deporte,name='ubicacion_cubierta_deporte'),
    path('usuarios/<str:deporte>',views.usuarios_deporte,name='usuarios_deporte'),
    path('buscador_calle/<str:palabra>', views.buscador_calle, name='buscador_calle'),
    path('equipo/<str:deporte>/<int:numero>', views.equipo_deporte_menos_jugadores, name='equipo_deporte_menos_jugadores'),
    path('jugador_libre', views.jugador_libre, name='jugador_libre'),
    path('ultimo_voto/<int:id_equipo>', views.ultimo_voto_equipo, name='ultimo_voto_equipo'),   
    path('equipos_votos/<int:id_usuario>',views.equipos_votos_superior_3_usuario, name='equipos_votos_superior_3_usuario') ,
    path('usuario_sin_voto', views.usuario_sin_voto, name='usuario_sin_voto'),
    path('cuentas_con_texto/<str:texto>', views.cuentas_con_texto, name='cuentas_con_texto'),
    path('media_votacion_superior', views.media_votacion_superior, name='media_votacion_superior'),
    path('crear_equipo', views.equipo_create, name='crear_equipo'),
    path('buscar/equipo',views.buscar_equipo,name='buscar_equipo'),
]