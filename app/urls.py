from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.indice, name='indice'),
    path('usuarios', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/<str:equipo>', views.usuarios_equipo, name='usuarios_equipo'),
    path('equipos', views.mostar_equipo, name='mostar_equipo'),
    path('lista_deportes', views.lista_deportes, name='lista_deportes'),
    path('usuarios_mayores/<int:edad>', views.usuarios_mayores, name='usuarios_mayores'),
    path('ubicacion', views.mostrar_ubicacion, name='listar_ubicacion'),
    path('ubicacion_cubierta/<str:deporte>', views.ubicacion_cubierta_deporte,name='ubicacion_cubierta_deporte'),
    path('usuarios/<str:deporte>',views.usuarios_deporte,name='usuarios_deporte'),
    path('buscador_calle/<str:palabra>', views.buscador_calle, name='buscador_calle'),
    path('equipo_mostrar/<str:deporte>/<int:numero>', views.equipo_deporte_menos_jugadores, name='equipo_deporte_menos_jugadores'),
    path('jugador_libre', views.jugador_libre, name='jugador_libre'),
    path('ultimo_voto/<int:id_equipo>', views.ultimo_voto_equipo, name='ultimo_voto_equipo'),   
    path('equipos_votos/<int:id_usuario>',views.equipos_votos_superior_3_usuario, name='equipos_votos_superior_3_usuario') ,
    path('usuario_sin_voto', views.usuario_sin_voto, name='usuario_sin_voto'),
    path('cuentas_con_texto/<str:texto>', views.cuentas_con_texto, name='cuentas_con_texto'),
    path('media_votacion_superior', views.media_votacion_superior, name='media_votacion_superior'),
    path('crear_equipo', views.equipo_create, name='crear_equipo'),
    path('buscar/equipo',views.buscar_equipo,name='buscar_equipo'),
    path('buscar_avanzado', views.equipo_buscar_avanzado, name='equipo_buscar_avanzado'),
    path('equipo/editar/<int:equipo_id>', views.equipo_editar, name='equipo_editar'),
    path('equipo/eliminar/<int:equipo_id>', views.equipo_eliminar, name='equipo_eliminar'),
    path('perfil_publico', views.mostrar_perfil_publico, name='listar_perfil_publico'),
    path('perfil_privado', views.mostrar_perfil_privado, name='listar_perfil_privado'),
    
    #--------------PROMOCION-----------
    path('crear_promocion', views.promocion_create, name='crear_promocion'),
    path('buscar/promocion', views.promocion_buscar_avanzado, name='promocion_buscar_avanzado'),
    path('promocion/actualizar/<int:promocion_id>', views.editar_promociones, name='editar_promociones'),
    path('promocion/borrar/<int:promocion_id>', views.borrar_promociones, name='borrar_promociones'),
    
    #--------------USUARIO-----------
    
    path('crear_usuario', views.usuario_create, name='crear_usuario'),
    path('buscar/usuario', views.usuario_buscar_avanzado, name='usuario_buscar_avanzado'),
    path('usuario/actualizar/<int:usuario_id>', views.editar_usuarios, name='editar_usuarios'),
    path('usuario/borrar/<int:usuario_id>', views.borrar_usuarios, name='borrar_usuarios'),
    
    #--------------UBICACION-----------
    path('crear_ubicacion', views.ubicacion_create, name='crear_ubicacion'),
    path('buscar/ubicacion', views.ubicacion_buscar_avanzado, name='ubicacion_buscar_avanzado'),
    path('ubicacion/actualizar/<int:ubicacion_id>', views.editar_ubicacion, name='editar_ubicacion'),
    path('ubicacion/borrar/<int:ubicacion_id>', views.borrar_ubicacion, name='borrar_ubicacion'),
    
    #--------------PERFIL PUBLICO-----------
    path('crear_perfil_publico', views.perfil_publico_create, name='crear_perfil_publico'),
    path('buscar/perfil_publico', views.perfil_publico_buscar_avanzado, name='perfil_publico_buscar_avanzado'),
    path('perfil_publico/actualizar/<int:perfil_publico_id>', views.editar_perfil_publico, name='editar_perfil_publico'),
    path('perfil_publico/borrar/<int:perfil_publico_id>', views.borrar_perfil_publico, name='borrar_perfil_publico'),
    
    #--------------PERFIL PRIVADO-----------
    path('crear_perfil_privado', views.perfil_privado_create, name='crear_perfil_privado'),
    path('buscar/perfil_privado', views.perfil_privado_buscar_avanzado, name='perfil_privado_buscar_avanzado'),
    path('perfil_privado/actualizar/<int:perfil_privado_id>', views.editar_perfil_privado, name='editar_perfil_privado'),
    path('perfil_privado/borrar/<int:perfil_privado_id>', views.borrar_perfil_privado, name='borrar_perfil_privado'),
]