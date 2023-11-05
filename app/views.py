from django.shortcuts import render
from django.db.models import Q, Prefetch
from .models import *

# Create your views here.

def indice(request):
    return render(request, 'index.html', {})

'''
Listado de todos los usuarios sin filtro
'''
def listar_usuarios(request):
    usuarios = Usuarios.objects.all()
    
    return render(request, 'usuario/listar_usuarios.html', {listar_usuarios:usuarios})


'''
Listado de todos los usuarios que practiquen un deporte en concreto, dado el nombre del deporte
'''
def usuarios_equipo(request, equipo):
    usuarios = Rel_Usu_Equi.objects.select_related('usuarios').select_related('equipos').filter(equipos=equipo).all()
    
    return render(request, 'usuario/usuarios_equipo.html', {usuarios_equipo:usuarios})


'''
Mostrar un equipos en especifico por id
'''
def mostar_equipo(request, id_equipo):
    equipos = Usuarios.objects.get(id=id_equipo)
    
    return render(request, 'equipo/mostar_equipo.html', {mostar_equipo:equipos})


'''
Mostar una lista con todos los deportes disponibles en la plataforma
'''
def lista_deportes(request):
    deportes = Deportes.objects.all()
    
    return render(request, 'deporte/lista_deportes.html',{lista_deportes:deportes})


'''
Mostar los usuarios mayores de cierta edad pasada como paramentro
'''
def usuarios_mayores(request, edad):
    usuarios = Usuarios.objects.filter(edad__gt=edad).all()
    
    return render(request, 'usuario/listar_usuarios.html',{usuarios_mayores:usuarios})

'''
Queremos las ubicaciones disponibles y tachadas para practicar x deporte
'''
def ubicacion_cubierta_deporte(request, deporte):
    ubicacion = Detalles_Ubicacion.objects.select_related('ubicacion').filter(cubierto=True).filter(ubicacion__deporte=deporte).all()
    
    return render(request, 'ubicacion/lista_ubicaciones.html',{ubicacion_cubierta_deporte:ubicacion})

'''
Lista de los usuarios cuyo deporte favorito sea el indicado
'''

def usuarios_deporte(request, deporte):
    usuarios = Perfil_Publico.objects.select_related('usuarios').filter(deportes_fav = deporte).all()
    
    return render(request, 'usuarios/listar_usuarios.html', {usuarios_deporte:usuarios})


'''
Devolver las ubicaciones cuya calle contenga el parametro de busqueda
'''
def buscador_calle(request, palabra):
    ubicacion = Ubicacion.objects.filter(calle__contains=palabra).all()
    
    return render (request, 'ubicacion/lista_ubicaciones.html', {buscador_calle:ubicacion})


'''
Devolver los equipos de x deporte con menos de "y" jugadores
'''
def equipo_deporte_menos_jugadores(request, deporte, numero):
    equipos = Equipos.objects.prefetch_related('deporte').filter(deporte__deporte=deporte).filter(capacidad__lt=numero)
    
    return render(request, 'equipo/lista_equipos.html',{equipo_deporte_menos_jugadores:equipos})


'''
Devoler jugadores sin asignar a ningun equipo
'''

def jugador_libre(request):
    usuario = Usuarios.objects.filter(rel_usu_equi=None).all()
    
    return render(request, 'usuario/listar_usuarios.html',{jugador_libre:usuario})


#Páginas de Error
def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
