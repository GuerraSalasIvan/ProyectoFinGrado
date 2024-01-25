from django.shortcuts import render, redirect
from django.db.models import Q, Prefetch, Avg
from .models import *
from .forms import *
from django.contrib import messages
from datetime import datetime

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
def mostar_equipo(request):
    equipos = Equipos.objects.all()
    
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
    
    return render(request, 'votacion/mostrar_votacion.html',{"voto":votacion})


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




'''
Formulario
'''

def equipo_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    formulario = EquiposModelForms(datosFormulario)

    if (request.method == "POST"):
         equipo_creado = crear_equipo_modelo(formulario)
         
         if(equipo_creado):
            messages.success(request, 'Se ha creado el equipo'+formulario.cleaned_data.get('nombre')+" correctamente")
            
            return redirect("crear_equipo")
        
    return render(request, 'equipo/crear.html',{"formulario":formulario})


def crear_equipo_modelo(formulario):
    equipo_creado = False
    
    if formulario.is_valid():
        equipo = Equipos.objects.create(
            nombre = formulario.cleaned_data.get('nombre'),
            capacidad = formulario.cleaned_data.get('capacidad'),
            deporte= formulario.cleaned_data.get('deporte'),
        )
        
        equipo.usuario_valoracion.set(formulario.cleaned_data.get('usuario_valoracion'))
        
        equipo.usurio.set(formulario.cleaned_data.get('usurio'))
        
        try:
            # Guarda el equipo en la base de datos
            equipo.save()
            equipo_creado = True
        except Exception as error:
            print(error)
    return equipo_creado


def buscar_equipo(request):
    formulario = BusquedaEquipoForm(request.GET)

    if formulario.is_valid():
        texto = formulario.cleaned_data.get('nombre')

        equipos = Equipos.objects.select_related('deporte').prefetch_related('usurio').filter(nombre__contains=texto).all()
        
        mensaje_busqueda =  "Se buscar por equipos que contienen en su nombre la palabra: " + texto
        
        return render(request, 'equipo/mostar_equipo.html',{"mostar_equipo":equipos,"texto_busqueda":mensaje_busqueda})
    
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
def equipo_buscar_avanzado(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaEquipoForm(request.GET)
        
        if formulario.is_valid():
            mensaje_busqueda = 'Se ha buscado por los siguientes valores:\n'
            
            equipos = Equipos.objects
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            deporte = formulario.cleaned_data.get('deporte')
            usuario = formulario.cleaned_data.get('usuario')
            capacidad  = formulario.cleaned_data.get('capacidad')
            
            if(textoBusqueda != ""):
                equipos = equipos.filter(Q(nombre__contains=textoBusqueda) | Q(deporte__deporte__contains=textoBusqueda))
                mensaje_busqueda +=" Nombre o deporte que contengan la palabra "+textoBusqueda+"\n"
            
            equipo = equipos.all()
            
            return render(request, 'equipo/mostar_equipo.html', {'mostar_equipo':equipo,'textoBusqueda':textoBusqueda })
            
    else:
        formulario = BusquedaAvanzadaEquipoForm(None)
    return render(request, 'equipo/busqueda_avanzada.html', {'formulario':formulario})
    

def equipo_editar(request,equipo_id):
    equipo = Equipos.objects.get(id=equipo_id)
    
    datosFormulario= None
    
    if request.method == 'POST':
        datosFormulario = request.POST
    
    formulario = EquiposModelForms(datosFormulario, instance=equipo)
    if request.method == 'POST':
        if formulario.is_valid():
            formulario.save()
            try:
                formulario.save()
                return redirect('mostar_equipo')
            except Exception as e:
                pass
    return render(request,'equipo/actualizar.html',{'formulario':formulario, 'equipo':equipo})


def equipo_eliminar(request,equipo_id):
    equipo = Equipos.objects.get(id=equipo_id)
    try:
        equipo.delete()
        messages.success(request, "Se ha elimnado el equipo "+equipo.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('mostar_equipo')
    





def promocion_buscar_avanzado(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaPromocionForm(request.GET)
        
        if formulario.is_valid():
            mensaje_busqueda = 'Se ha buscado por los siguientes valores:\n'
            
            promocion = Promocion.objects
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            rangoDescuento = formulario.cleaned_data.get('rangoDescuento')
            usuarios = formulario.cleaned_data.get('usuarios')
            fechaDesde = formulario.cleaned_data.get('fecha_desde')
            fechaHasta = formulario.cleaned_data.get('fecha_hasta')
       
            
            if(textoBusqueda != ""):
                promocion = promocion.filter(Q(nombre__contains=textoBusqueda) | Q(descripcion__contains=textoBusqueda))
                mensaje_busqueda +=" Nombre o deporte que contengan la palabra "+textoBusqueda+"\n"
            
            #filtro para que busque descuento mayor 
            if(not rangoDescuento is None):
                promocion = promocion.filter(descuento__gt=rangoDescuento)
                
            #filtros de para los usuarios, en caso de que sean mas de uno o de q sea uno
            if(len(usuarios) > 0):
                filtroOR = Q(usuarios = usuarios[0])
                for usuario in usuarios[1:]:
                    filtroOR |= Q(usuarios=usuario)
            
                promocion = promocion.filter(filtroOR)
            
            
            #filtros de la fecha
            if(not fechaDesde is None):
                mensaje_busqueda +=" La fecha sea mayor a "+datetime.strftime(fechaDesde,'%d-%m-%Y')+"\n"
                promocion = promocion.filter(fecha_fin_promocion__gte=fechaDesde)
            
             
            if(not fechaHasta is None):
                mensaje_busqueda +=" La fecha sea menor a "+datetime.strftime(fechaHasta,'%d-%m-%Y')+"\n"
                promocion = promocion.filter(fecha_fin_promocion__lte=fechaHasta)
                
            promocion = promocion.all()
            
            return render(request, 'promocion/mostar_promocion.html', {'mostar_promocion':promocion,'textoBusqueda':textoBusqueda })
            
    else:
        formulario = BusquedaAvanzadaPromocionForm(None)
    return render(request, 'promocion/busqueda_promocion.html', {'formulario':formulario})

#metodo para editar las promociones
def editar_promociones(request, promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    
    datosFormulario=None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = PromocionModelForm(datosFormulario,instance = promocion)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
            except Exception as error:
                print(error)
                
    return render(request, 'promocion/actualizar.html',{"formulario":formulario,"promocion":promocion})

#borrar la promocion
def borrar_promociones(request, promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    try:
        promocion.delete()
        messages.success(request, "Se ha elimnado el equipo "+promocion.nombre+" correctamente")
    except Exception as error:
        print(error)
        #como no tengo una vista 'mostrar promocion' lo redirijo al buscador, aqui desde ahi si se pueden ver 
    return redirect('promocion_buscar_avanzado')




#Páginas de Error
def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
