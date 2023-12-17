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

def mostrar_ubicacion(request):
    ubicacion = Ubicacion.objects.all()
    
    return render(request, 'ubicacion/lista_ubicaciones.html',{'ubicacion_cubierta_deporte':ubicacion})


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

def mostrar_perfil_publico(request):

    perfil_publico = Perfil_Publico.objects.all()

    return render(request, 'perfil_publico/lista_perfil_publico.html',{'perfil_publico':perfil_publico})

def mostrar_perfil_privado(request):

    perfil_privado = Perfil_Privado.objects.all()

    return render(request, 'perfil_privado/lista_perfil_privado.html',{'perfil_privado':perfil_privado})


'''
Formulario
'''
#--------------------------------EQUIPO---------------------------------------------------------------------

def equipo_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    formulario = EquiposModelForms(datosFormulario)

    if (request.method == "POST"):
         equipo_creado = crear_equipo_modelo(formulario)
         
         if(equipo_creado):
            messages.success(request, 'Se ha creado el equipo'+formulario.cleaned_data.get('nombre')+" correctamente")
            
            return redirect("mostar_equipo")
        
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
        messages.success(request, "Se ha elimnado el libro "+equipo.nombre+" correctamente")
    except Exception as error:
        print(error)
    return redirect('mostar_equipo')
    


#--------------------------------promocion---------------------------------------------------------------------
#crear modelo promocion
def promocion_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    formulario = PromocionModelForm(datosFormulario)

    if (request.method == "POST"):
         promocion_creado = crear_promocion_modelo(formulario)
         
         if(promocion_creado):
            messages.success(request, 'Se ha creado la promocion'+formulario.cleaned_data.get('nombre')+" correctamente")
            
            return redirect("crear_promocion")
        
    return render(request, 'promocion/crear.html',{"formulario":formulario})


#crear promocion
def crear_promocion_modelo(formulario):
    promocion_creado = False
    
    if formulario.is_valid():
        promocion = Promocion.objects.create(
            nombre = formulario.cleaned_data.get('nombre'),
            descripcion = formulario.cleaned_data.get('descripcion'),
            descuento= formulario.cleaned_data.get('descuento'),
            fecha_fin_promocion = formulario.cleaned_data.get('fecha_fin_promocion'),
            promocions = formulario.cleaned_data.get('promocions')
        )
    
        
        try:
            # Guarda el equipo en la base de datos
            promocion.save()
            promocion_creado = True
        except Exception as error:
            print(error)
    return promocion_creado


#busqueda avanzada promocion
def promocion_buscar_avanzado(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaPromocionForm(request.GET)
        
        if formulario.is_valid():
            mensaje_busqueda = 'Se ha buscado por los siguientes valores:\n'
            
            promocion = Promocion.objects
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            rangoDescuento = formulario.cleaned_data.get('rangoDescuento')
            promocions = formulario.cleaned_data.get('promocions')
            fechaDesde = formulario.cleaned_data.get('fecha_desde')
            fechaHasta = formulario.cleaned_data.get('fecha_hasta')
       
            
            if(textoBusqueda != ""):
                promocion = promocion.filter(Q(nombre__contains=textoBusqueda) | Q(descripcion__contains=textoBusqueda))
                mensaje_busqueda +=" Nombre o deporte que contengan la palabra "+textoBusqueda+"\n"
            
            #filtro para que busque descuento mayor 
            if(not rangoDescuento is None):
                promocion = promocion.filter(descuento__gt=rangoDescuento)
                
            #filtros de para los promocions, en caso de que sean mas de uno o de q sea uno
            if(len(promocions) > 0):
                filtroOR = Q(promocions = promocions[0])
                for promocion in promocions[1:]:
                    filtroOR |= Q(promocions=promocion)
            
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
                return redirect('crear_promocion')
            except Exception as error:
                print(error)
                
    return render(request, 'promocion/actualizar.html',{"formulario":formulario,"promocion":promocion})

#borrar la promocion
def borrar_promociones(request, promocion_id):
    promocion = Promocion.objects.get(id=promocion_id)
    try:
        promocion.delete()
        messages.success(request, "Se ha elimnado la promocion "+promocion.nombre+" correctamente")
    except Exception as error:
        print(error)
        #como no tengo una vista 'mostrar promocion' lo redirijo al buscador, aqui desde ahi si se pueden ver 
    return redirect('promocion_buscar_avanzado')


#--------------------------------USUARIOS---------------------------------------------------------------------
#crear modelo usuario
def usuario_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    formulario = UsuarioModelForm(datosFormulario)

    if (request.method == "POST"):
         usuario_creado = crear_usuario_modelo(formulario)
         
         if(usuario_creado):
            messages.success(request, 'Se ha creado el usuario'+formulario.cleaned_data.get('nombre')+" correctamente")
            
            return redirect("listar_usuarios")
        
    return render(request, 'usuario/crear.html',{"formulario":formulario})



#crear usuario
def crear_usuario_modelo(formulario):
    usuario_creado = False
    
    if formulario.is_valid():
        usuario = Usuarios.objects.create(
            nombre = formulario.cleaned_data.get('nombre'),
            apellidos = formulario.cleaned_data.get('apellidos'),
            edad= formulario.cleaned_data.get('edad'),
            sexo = formulario.cleaned_data.get('sexo'),
        )
        try:
            # Guarda el equipo en la base de datos
            usuario.save()
            usuario_creado = True
        except Exception as error:
            print(error)
    return usuario_creado


#busqueda avanzada usuario
def usuario_buscar_avanzado(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaUsuarioForm(request.GET)
        
        if formulario.is_valid():
            mensaje_busqueda = 'Se ha buscado por los siguientes valores:\n'
            
            usuario = Usuarios.objects
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            rangoEdad = formulario.cleaned_data.get('rangoEdad')
            sexo = formulario.cleaned_data.get('sexo')
            
            if(textoBusqueda != ""):
                usuario = usuario.filter(Q(nombre__contains=textoBusqueda) | Q(apellidos__contains=textoBusqueda))
                mensaje_busqueda +=" Nombre o deporte que contengan la palabra "+textoBusqueda+"\n"
            
            #filtro para que busque descuento mayor 
            if(not rangoEdad is None):
                usuario = usuario.filter(edad=rangoEdad)
                
            #filtro para que busque por sexo
            if(not sexo is None):
                usuario = usuario.filter(sexo=sexo)
            
            usuario = usuario.all()
            
            return render(request, 'usuario/listar_usuarios.html', {'listar_usuarios':usuario,'textoBusqueda':textoBusqueda })
            
    else:
        formulario = BusquedaAvanzadaUsuarioForm(None)
    return render(request, 'usuario/busqueda_usuario.html', {'formulario':formulario})
            

#metodo para editar las usuario
def editar_usuarios(request, usuario_id):
    usuario = Usuarios.objects.get(id=usuario_id)
    
    datosFormulario=None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = UsuarioModelForm(datosFormulario,instance = usuario)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                return redirect('listar_usuarios')
            except Exception as error:
                print(error)
                
    return render(request, 'usuario/actualizar.html',{"formulario":formulario,"usuario":usuario})

#borrar usuario
def borrar_usuarios(request, usuario_id):
    usuario = Usuarios.objects.get(id=usuario_id)
    try:
        usuario.delete()
        messages.success(request, "Se ha elimnado el usuario "+usuario.nombre+" correctamente")
    except Exception as error:
        print(error)
        #como no tengo una vista 'mostrar usuario' lo redirijo al buscador, aqui desde ahi si se pueden ver 
    return redirect('listar_usuarios')


#--------------------------------UBICACION---------------------------------------------------------------------
#crear modelo ubicacion
def ubicacion_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    formulario = UbicacionModelForm(datosFormulario)

    if (request.method == "POST"):
         ubicacion_creado = crear_ubicacion_modelo(formulario)
         
         if(ubicacion_creado):
            messages.success(request, 'Se ha creado el ubicacion'+formulario.cleaned_data.get('nombre')+" correctamente")
            
            return redirect("listar_ubicacion")
        
    return render(request, 'ubicacion/crear.html',{"formulario":formulario})


#crear ubicacion
def crear_ubicacion_modelo(formulario):
    ubicacion_creado = False
    
    if formulario.is_valid():
        ubicacion = Ubicacion.objects.create(
            nombre = formulario.cleaned_data.get('nombre'),
            capacidad = formulario.cleaned_data.get('capacidad'),
            calle = formulario.cleaned_data.get('calle'),
            
        )
        #Añadir los equipos y deportes (manyToMany)
        ubicacion.equipo.set(formulario.cleaned_data.get('equipo'))
        ubicacion.deporte.set(formulario.cleaned_data.get('deporte'))
        
        try:
            # Guarda el equipo en la base de datos
            ubicacion.save()
            ubicacion_creado = True
        except Exception as error:
            print(error)
    return ubicacion_creado

#busqueda avanzada ubicacion
def ubicacion_buscar_avanzado(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaUbicacionForm(request.GET)
        
        if formulario.is_valid():
            mensaje_busqueda = 'Se ha buscado por los siguientes valores:\n'
            
            ubicacion = Ubicacion.objects
            
            textoBusqueda = formulario.cleaned_data.get('textoBusqueda')
            capacidad = formulario.cleaned_data.get('capacidad')
            calle = formulario.cleaned_data.get('calle')
            equipo = formulario.cleaned_data.get('equipo')
            deporte = formulario.cleaned_data.get('deporte')
       
            
            if(textoBusqueda != ""):
                ubicacion = ubicacion.filter(Q(nombre__contains=textoBusqueda) | Q(calle__contains=textoBusqueda))
                mensaje_busqueda +=" Nombre o deporte que contengan la palabra "+textoBusqueda+"\n"
            
            #filtro para que busque mas capacidad de la indicada
            if(not capacidad is None):
                ubicacion = ubicacion.filter(capacidad__gt=capacidad)
                
            #filtros de para los equipo, en caso de que sean mas de uno o de q sea uno
            if(len(equipo) > 0):
                filtroOR = Q(equipo = equipo[0])
                for equipo in equipo[1:]:
                    filtroOR |= Q(equipo=equipo)
            
                ubicacion = ubicacion.filter(filtroOR)
                
                     #filtros de para los equipo, en caso de que sean mas de uno o de q sea uno
            if(len(deporte) > 0):
                filtroOR = Q(deporte = deporte[0])
                for deporte in deporte[1:]:
                    filtroOR |= Q(deporte=deporte)
            
                ubicacion = ubicacion.filter(filtroOR)
            
            ubicacion = ubicacion.all()
            
            return render(request, 'ubicacion/lista_ubicaciones.html', {'ubicacion_cubierta_deporte':ubicacion,'textoBusqueda':textoBusqueda })
            
    else:
        formulario = BusquedaAvanzadaUbicacionForm(None)
    return render(request, 'ubicacion/busqueda_ubicacion.html', {'formulario':formulario})


#metodo para editar las ubicaciones
def editar_ubicacion(request, ubicacion_id):
    ubicacion = Ubicacion.objects.get(id=ubicacion_id)
    
    datosFormulario=None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = UbicacionModelForm(datosFormulario,instance = ubicacion)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                return redirect('listar_ubicacion')
            except Exception as error:
                print(error)
                
    return render(request, 'ubicacion/actualizar.html',{"formulario":formulario,"ubicacion":ubicacion})

#borrar ubicacion
def borrar_ubicacion(request, ubicacion_id):
    ubicacion = Ubicacion.objects.get(id=ubicacion_id)
    try:
        ubicacion.delete()
        messages.success(request, "Se ha elimnado la ubicacion "+ubicacion.nombre+" correctamente")
    except Exception as error:
        print(error)
        #como no tengo una vista 'mostrar ubicacion' lo redirijo al buscador, aqui desde ahi si se pueden ver 
    return redirect('listar_ubicacion')

#--------------------------------PERFIL PUBLICO---------------------------------------------------------------------
#crear modelo perfil_publico
def perfil_publico_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    formulario = PerfilPublicoModelForm(datosFormulario)

    if (request.method == "POST"):
         perfil_publico_creado = crear_perfil_publico_modelo(formulario)
         
         if(perfil_publico_creado):
            messages.success(request, 'Se ha creado el perfil_publico de '+str(formulario.cleaned_data.get('usuarios'))+" correctamente")
            
            return redirect("listar_perfil_publico")
        
    return render(request, 'perfil_publico/crear.html',{"formulario":formulario})


#crear perfil_publico
def crear_perfil_publico_modelo(formulario):
    perfil_publico_creado = False
    
    if formulario.is_valid():
        perfil_publico = Perfil_Publico.objects.create(
            descripcion = formulario.cleaned_data.get('descripcion'),
            lugar_fav = formulario.cleaned_data.get('lugar_fav'),
            deportes_fav = formulario.cleaned_data.get('deportes_fav'),
            hitos_publicos = formulario.cleaned_data.get('hitos_publicos'),
            usuarios = formulario.cleaned_data.get('usuarios'), 
        )

        
        try:
            # Guarda el equipo en la base de datos
            perfil_publico.save()
            perfil_publico_creado = True
        except Exception as error:
            print(error)
    return perfil_publico_creado

#busqueda avanzada perfil_publico
def perfil_publico_buscar_avanzado(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaPerfilPublicoForm(request.GET)
        
        if formulario.is_valid():
            mensaje_busqueda = 'Se ha buscado por los siguientes valores:\n'
            
            perfil_publico = Perfil_Publico.objects
            
            descripcion = formulario.cleaned_data.get('descripcion')
            lugar_fav = formulario.cleaned_data.get('lugar_fav')
            hitos_publicos = formulario.cleaned_data.get('hitos_publicos')
            usuarios = formulario.cleaned_data.get('usuarios')
       
            
            if(descripcion != ""):
                perfil_publico = perfil_publico.filter(descripcion__contains=descripcion)
                mensaje_busqueda +=" descripcion de Perfil Publico que contengan la palabra "+descripcion+"\n"
                
            if(hitos_publicos != ""):
                perfil_publico = perfil_publico.filter(hitos_publicos__contains=hitos_publicos)
                mensaje_busqueda +=" hitos_publicos de Perfil Publico que contengan la palabra "+hitos_publicos+"\n"
            

            #filtros de para los usuarios, en caso de que sean mas de uno o de q sea uno
            if(len(usuarios) > 0):
                filtroOR = Q(usuarios = usuarios[0])
                for usuarios in usuarios[1:]:
                    filtroOR |= Q(usuarios=usuarios)
                    
            #filtros de para los usuarios, en caso de que sean mas de uno o de q sea uno
            if(len(lugar_fav) > 0):
                filtroOR = Q(lugar_fav = lugar_fav[0])
                for lugar_fav in lugar_fav[1:]:
                    filtroOR |= Q(lugar_fav=lugar_fav)
            
                perfil_publico = perfil_publico.filter(filtroOR)
                
    
            perfil_publico = perfil_publico.all()
            
            return render(request, 'perfil_publico/lista_perfil_publico.html', {'perfil_publico':perfil_publico,'textoBusqueda':descripcion})
            
    else:
        formulario = BusquedaAvanzadaPerfilPublicoForm(None)
    return render(request, 'perfil_publico/busqueda_perfil_publico.html', {'formulario':formulario})



#metodo para editar las perfil_publico
def editar_perfil_publico(request, perfil_publico_id):
    perfil_publico = Perfil_Publico.objects.get(id=perfil_publico_id)
    
    datosFormulario=None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = PerfilPublicoModelForm(datosFormulario,instance = perfil_publico)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                return redirect('listar_perfil_publico')
            except Exception as error:
                print(error)
                
    return render(request, 'perfil_publico/actualizar.html',{"formulario":formulario,"perfil_publico":perfil_publico})

#borrar perfil_publico
def borrar_perfil_publico(request, perfil_publico_id):
    perfil_publico = Perfil_Publico.objects.get(id=perfil_publico_id)
    try:
        perfil_publico.delete()
        messages.success(request, "Se ha elimnado el perfil publico de "+perfil_publico.usuarios+" correctamente")
    except Exception as error:
        print(error)
        #como no tengo una vista 'mostrar perfil_publico' lo redirijo al buscador, aqui desde ahi si se pueden ver 
    return redirect('listar_perfil_publico')

#--------------------------------PERFIL PRIVADO---------------------------------------------------------------------
#crear modelo perfil_privado
def perfil_privado_create(request):
    datosFormulario = None
    if request.method == "POST":
        datosFormulario = request.POST
    formulario = PerfilPrivadoModelForm(datosFormulario)

    if (request.method == "POST"):
         perfil_privado_creado = crear_perfil_privado_modelo(formulario)
         
         if(perfil_privado_creado):
            messages.success(request, 'Se ha creado el perfil_privado de '+str(formulario.cleaned_data.get('usuarios'))+" correctamente")
            
            return redirect("listar_perfil_privado")
        
    return render(request, 'perfil_privado/crear.html',{"formulario":formulario})


#crear perfil_privado
def crear_perfil_privado_modelo(formulario):
    perfil_privado_creado = False
    
    if formulario.is_valid():
        perfil_privado = Perfil_Privado.objects.create(
            historial_trayectoria = formulario.cleaned_data.get('historial_trayectoria'),
            incidencias = formulario.cleaned_data.get('incidencias'),
            hitos = formulario.cleaned_data.get('hitos'),
            usuarios = formulario.cleaned_data.get('usuarios'),
        )
        
        try:
            # Guarda el equipo en la base de datos
            perfil_privado.save()
            perfil_privado_creado = True
        except Exception as error:
            print(error)
    return perfil_privado_creado

#busqueda avanzada perfil_privado
def perfil_privado_buscar_avanzado(request):
    pass

#metodo para editar las perfil_privado
def editar_perfil_privado(request, perfil_privado_id):
    perfil_privado = Perfil_Privado.objects.get(id=perfil_privado_id)
    
    datosFormulario=None
    
    if request.method == "POST":
        datosFormulario = request.POST
        
    formulario = PerfilPrivadoModelForm(datosFormulario,instance = perfil_privado)
    
    if (request.method == "POST"):
       
        if formulario.is_valid():
            try:  
                formulario.save()
                return redirect('listar_perfil_privado')
            except Exception as error:
                print(error)
                
    return render(request, 'perfil_privado/actualizar.html',{"formulario":formulario,"perfil_privado":perfil_privado})


#borrar perfil_privado
def borrar_perfil_privado(request, perfil_privado_id):
    perfil_privado = Perfil_Privado.objects.get(id=perfil_privado_id)
    try:
        perfil_privado.delete()
        messages.success(request, "Se ha elimnado el perfil privado de "+perfil_privado.usuarios+" correctamente")
    except Exception as error:
        print(error)
        #como no tengo una vista 'mostrar perfil_privado' lo redirijo al buscador, aqui desde ahi si se pueden ver 
    return redirect('listar_perfil_privado')



#Páginas de Error
def mi_error_400(request,exception=None):
    return render(request, 'errores/400.html',None,None,400)

def mi_error_403(request,exception=None):
    return render(request, 'errores/403.html',None,None,403)

def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)
