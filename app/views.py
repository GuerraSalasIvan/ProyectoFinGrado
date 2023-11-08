from django.shortcuts import render
from django.db.models import Q, Prefetch, Avg
from .models import *

# Create your views here.

def indice(request):
    return render(request, 'index.html', {})

'''
Listado de todos los usuarios sin filtro
'''
def listar_usuarios(request):
    usuarios = Usuarios.objects.all()
    
    return render(request, 'usuario/listar_usuarios.html', {"listar_usuarios":usuarios})


'''
Listado de todos los usuarios que practiquen un deporte en concreto, dado el nombre del deporte
'''
def usuarios_equipo(request, equipo):
    usuarios = Rel_Usu_Equi.objects.select_related('usuario').select_related('equipos').filter(equipos=equipo).all()
    
    return render(request, 'usuario/usuarios_equipo.html', {"usuarios_equipo":usuarios})


'''
Mostrar un equipos en especifico por id
'''
def mostar_equipo(request, id_equipo):
    equipos = Usuarios.objects.get(id=id_equipo)
    
    return render(request, 'equipo/mostar_equipo.html', {"mostar_equipo":equipos})


'''
Mostar una lista con todos los deportes disponibles en la plataforma
'''
def lista_deportes(request):
    deportes = Deportes.objects.all()
    
    return render(request, 'deporte/lista_deportes.html',{"lista_deportes":deportes})


'''
Mostar los usuarios mayores de cierta edad pasada como paramentro
'''
def usuarios_mayores(request, edad):
    usuarios = Usuarios.objects.filter(edad__gt=edad).all()
    
    return render(request, 'usuario/listar_usuarios.html',{"listar_usuarios":usuarios})

'''
Queremos las ubicaciones disponibles y tachadas para practicar x deporte
'''
def ubicacion_cubierta_deporte(request, deporte):
    ubicacion = Detalles_Ubicacion.objects.select_related('ubicacion').filter(cubierto=True).filter(ubicacion__deporte=deporte).all()
    
    return render(request, 'ubicacion/lista_ubicaciones.html',{"ubicacion_cubierta_deporte":ubicacion})


'''
Lista de los usuarios cuyo deporte favorito sea el indicado
'''
def usuarios_deporte(request, deporte):
    usuarios = Perfil_Publico.objects.select_related('usuarios').filter(deportes_fav = deporte).all()
    
    return render(request, 'usuarios/listar_usuarios.html', {"usuarios_deporte":usuarios})


'''
Devolver las ubicaciones cuya calle contenga el parametro de busqueda
'''
def buscador_calle(request, palabra):
    ubicacion = Ubicacion.objects.filter(calle__contains=palabra).all()
    
    return render (request, 'ubicacion/lista_ubicaciones.html', {"buscador_calle":ubicacion})


'''
Devolver los equipos de x deporte con menos de "y" jugadores
'''
def equipo_deporte_menos_jugadores(request, deporte, numero):
    equipos = Equipos.objects.prefetch_related('deporte').filter(deporte__deporte=deporte).filter(capacidad__lt=numero)
    
    return render(request, 'equipo/lista_equipos.html',{"equipo_deporte_menos_jugadores":equipos})


'''
Devoler jugadores sin asignar a ningun equipo
'''
def jugador_libre(request):
    usuario = Usuarios.objects.filter(rel_usu_equi=None).all()
    
    return render(request, 'usuario/listar_usuarios.html',{"listar_usuarios":usuario})


'''
El último voto que se realizó en un modelo principal en concreto, y mostrar el comentario, la votación e información del usuario o cliente que lo realizó.
'''
def ultimo_voto_equipo(request, id_equipo):
    votacion=(Votacion.objects.select_related('usuarios','equipos')
              .filter(equipos=id_equipo)
              .order_by('-fecha')[:1]
              .get())
    
    return render(request, 'votacion/mostrar_votacion.html',{"mostrar_votacion":votacion})


'''
Todos los modelos principales que tengan votos con una puntuación numérica igual a 3 y que realizó un usuario o cliente en concreto. 
'''
def equipos_votos_superior_3_usuario(request, id_usuario):
    votacion = (Votacion.objects.select_related('usuarios','equipos')
                .filter(usuarios=id_usuario)
                .filter(puntuacion__gte=3)
                .all())
    
    return render(request, 'votacion/listar_votacion.html',{"listar_votacion":votacion})


'''
Todos los usuarios o clientes que no han votado nunca y mostrar información sobre estos usuarios y clientes al completo.
'''
def usuario_sin_voto(request):
    usuarios = Usuarios.objects.filter(votacion=None).all()

    return render(request, 'usuario/listar_usuarios.html', {"listar_usuarios":usuarios})



'''
Obtener las cuentas bancarias que sean de la Caixa o de Unicaja y que el propietario tenga un nombre que contenga un texto en concreto, por ejemplo “Juan”.
'''

def cuentas_con_texto(request, texto):
    cuenta = (CuentaBancaria.objects.select_related('usuario')
              .filter(Q(nombre='Caixa') | Q(nombre='UNICAJA'))
              .filter(usuario__nombre__contains=texto)
              .all())
    
    return render(request, 'cuenta/listar_cuentas.html', {"listar_cuentas":cuenta})


'''
Obtener todos los modelos principales que tengan una media de votaciones mayor del 2,5.
'''
def media_votacion_superior(request):
 
    
    votacion=(Votacion.objects.select_related('usuarios','equipos')
              .annotate(puntuacion__avg=Avg('puntuacion',default=0))
              .filter(puntuacion__avg__gte=2.5).all())
    
    return render(request, 'votacion/media_votacion.html',{'listar_votacion':votacion})

#Páginas de Error
def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
