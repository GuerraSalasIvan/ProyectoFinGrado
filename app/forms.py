from django.forms import ModelForm
from django import forms
from .models import *
from datetime import date
import datetime

#--------------------------------EQUIPO---------------------------------------------------------------------
class EquiposModelForms(ModelForm):
    class Meta:
        model = Equipos
        fields = ['nombre','capacidad','deporte','usuario_valoracion','usurio']
        
        label = {
            'nombre':{'Nombre del equipo'},
            'capacidad':{'Numero máximo de integrantes'},
            'deporte':{'Deporte'},
            'usuario_valoracion':{'Valoraciones'},
            'usurio':{'creador'}
        }
        
        help_texts = {
            'nombre':{'Nombre'},
            'capacidad':{'Integrantes'},
            'usuario_valoracion':{'Valoraciones'},
            'usurio':{'creador'}
        }
    
    
    def clean(self):
        
        super().clean()
        
        #Obtener los campos
        nombre = self.cleaned_data.get('nombre')
        capacidad = self.cleaned_data.get('capacidad')
        deporte= self.cleaned_data.get('deporte')
        usuario_valoracion = self.cleaned_data.get('usuario_valoracion')
        usurio = self.cleaned_data.get('usurio')

        #Validator de nombre de equipo
        equipoNombre = Equipos.objects.filter(nombre=nombre).first()
        if(not equipoNombre is None):
            self.add_error('nombre','Ya existe un equipo con ese nombre')

        #Validator capacidad
        if(capacidad > 20):
            self.add_error('capacidad','No puede haber mas de 20 miembros')
            
class BusquedaEquipoForm(forms.Form):
    nombre = forms.CharField(required=False)
    


class BusquedaAvanzadaEquipoForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)

    def clean(self):
        super().clean()
        
        #Obtenemos los campos
        textoBusqueda = self.cleaned_data.get('textoBusqueda')

        if(textoBusqueda == ""):
             self.add_error('textoBusqueda', 'no textoBusqueda')
        
        return self.cleaned_data
    





#--------------------------------PROMOCION---------------------------------------------------------------------
        
class BusquedaAvanzadaPromocionForm(forms.Form):
    
    usuariosdisponibles=Usuarios.objects.all()
    
    #creamos el formulario
    textoBusqueda = forms.CharField(required=False)
    rangoDescuento = forms.IntegerField(required=False)
    usuarios = forms.ModelMultipleChoiceField(queryset=usuariosdisponibles, widget=forms.SelectMultiple, required=False)
    fecha_desde = forms.DateField(label="Fecha Desde",
                                required=False,
                                widget= forms.SelectDateWidget(years=range(2020,2024))
                                )
    
    fecha_hasta = forms.DateField(label="Fecha Hasta",
                                  required=False,
                                  widget= forms.SelectDateWidget(years=range(2020,2024))
                                  )
    

    def clean(self):
        super().clean()
        
        #Obtenemos los campos
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        rangoDescuento = self.cleaned_data.get('rangoDescuento')
        usuarios = self.cleaned_data.get('usuarios')
        fecha_desde = self.cleaned_data.get('fecha_desde')
        fecha_hasta = self.cleaned_data.get('fecha_hasta')

        #al menos tiene que poner un campo
        if(textoBusqueda == ""
           and rangoDescuento is None
           and len(usuarios) == 0
           and fecha_desde is None
           and fecha_hasta is None):
             self.add_error('textoBusqueda', 'no textoBusqueda')
             self.add_error('rangoDescuento', 'no rangoDescuento')
             self.add_error('usuarios', 'no hay usuarios')
             self.add_error('fecha_desde','Debe introducir al menos un valor en un campo del formulario')
             self.add_error('fecha_hasta','Debe introducir al menos un valor en un campo del formulario')

        #solo permitir rango de 0 a 100
        else:
            if (not(rangoDescuento is None) and (rangoDescuento < 0 and rangoDescuento > 100)):
                self.add_error('rangoDescuento', 'debe estar entre 0 y 100')
                
                
            if(not fecha_desde is None  and not fecha_hasta is None and fecha_hasta < fecha_desde):
                self.add_error('fecha_desde','La fecha hasta no puede ser menor que la fecha desde')
                self.add_error('fecha_hasta','La fecha hasta no puede ser menor que la fecha desde')
        
        return self.cleaned_data
    
    #Vamos a crear un create rapido
class PromocionModelForm(ModelForm):
    class Meta:
        model = Promocion
        fields = ['nombre','descripcion','descuento','fecha_fin_promocion','usuarios',]
        labels = {
            "nombre": ("Nombre promocion"),
        }
        widgets = {
            "fecha_fin_promocion":forms.SelectDateWidget(),
            
        }

    def clean(self):
 
        #Validamos con el modelo actual
        super().clean()
        
        nombre = self.cleaned_data.get('nombre')
        descripcion = self.cleaned_data.get('descripcion')
        
        #Comprobamos que no exista una promocion con ese nombre
        PromocionNombre = Promocion.objects.filter(nombre=nombre).first()
        if(not PromocionNombre is None
           ):
             if(not self.instance is None and PromocionNombre.id == self.instance.id):
                 pass
             else:
                self.add_error('nombre','Ya existe una promocion con ese nombre')
        
        return self.cleaned_data
    
    
#--------------------------------USUARIOS---------------------------------------------------------------------
 
#Create de usuarios
class UsuarioModelForm(ModelForm):
    class Meta:
        model = Usuarios
        fields = ['nombre','apellidos','edad','sexo']
        labels = {
            "nombre": ("Nombre usuario"),
        }
        

    def clean(self):
 
        #Validamos con el modelo actual
        super().clean()
        
        nombre = self.cleaned_data.get('nombre')
        apellidos = self.cleaned_data.get('apellidos')
        edad=self.cleaned_data.get('edad')
        sexo=self.cleaned_data.get('sexo')
        
        #Comprobamos que no exista una promocion con ese nombre
        UsuarioNombre = Usuarios.objects.filter(nombre=nombre).first()
        if(not UsuarioNombre is None
           ):
             if(not self.instance is None and UsuarioNombre.id == self.instance.id):
                 pass
             else:
                self.add_error('nombre','Ya existe un usuario con ese nombre')
        
        return self.cleaned_data
    

#--------------------------------Ubicacion---------------------------------------------------------------------

#Create de Ubicacion
class UbicacionModelForm(ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['nombre','capacidad','calle','equipo','deporte']
        labels = {
            "nombre": ("Nombre Ubicacion"),
        }
        

    def clean(self):
 
        #Validamos con el modelo actual
        super().clean()
        
        nombre = self.cleaned_data.get('nombre')
        capacidad = self.cleaned_data.get('capacidad')
        calle=self.cleaned_data.get('calle')
        equipo=self.cleaned_data.get('equipo')
        deporte=self.cleaned_data.get('deporte')
        
        
        #Comprobamos que no exista una ubicacion en ese calle exacta (puede en la misma calle, pero no exacta, es decir, el string entero con el numero de la calle)
        UbicacionCalle = Ubicacion.objects.filter(calle=calle).first()
        if(not UbicacionCalle is None
           ):
             if(not self.instance is None and UbicacionCalle.id == self.instance.id):
                 pass
             else:
                self.add_error('nombre','Ya existe una Ubicacion en esa Calle')
        
        return self.cleaned_data
        
    
#--------------------------------PERFIL PUBLICO---------------------------------------------------------------------
#Create de Perfil Publico
class PerfilPublicoModelForm(ModelForm):
    class Meta:
        model = Perfil_Publico
        fields = ['descripcion','lugar_fav','deportes_fav','hitos_publicos','usuarios']
        labels = {
            "descripcion": ("Descripcion"),
            "lugar_fav": ("Lugar favorito"),
            "deportes_fav": ("Deportes favorito"),
        }
        

    def clean(self):
 
        #Validamos con el modelo actual
        super().clean()
        
        descripcion = self.cleaned_data.get('descripcion')
        lugar_fav = self.cleaned_data.get('lugar_fav')
        deportes_fav=self.cleaned_data.get('deportes_fav')
        hitos_publicos=self.cleaned_data.get('hitos_publicos')
        usuarios=self.cleaned_data.get('usuarios')
        
        
        #Comprobamos que no exista una ubicacion en ese calle exacta (puede en la misma calle, pero no exacta, es decir, el string entero con el numero de la calle)
        UsuarioRepetido = Perfil_Publico.objects.filter(usuarios=usuarios).first()
        if(not UsuarioRepetido is None
           ):
             if(not self.instance is None and UsuarioRepetido.id == self.instance.id):
                 pass
             else:
                self.add_error('usuarios','Este usuario ya tiene un perfil publico')
        
        return self.cleaned_data

#--------------------------------PERFIL PRIVADO---------------------------------------------------------------------
#Create de Perfil Privado
class PerfilPrivadoModelForm(ModelForm):
    class Meta:
        model = Perfil_Privado
        fields = ['historial_trayectoria','incidencias','hitos','usuarios']
        labels = {
            "historial_trayectoria": ("¿En que equipos has estado anteriormente?"),
            "incidencias": ("Incidencias"),
            "hitos": ("Hitos"),
        }
        

    def clean(self):
 
        #Validamos con el modelo actual
        super().clean()
        
        historial_trayectoria = self.cleaned_data.get('historial_trayectoria')
        incidencias = self.cleaned_data.get('incidencias')
        hitos=self.cleaned_data.get('hitos')
        usuarios=self.cleaned_data.get('usuarios')
        
        
        #Comprobamos que no exista una ubicacion en ese calle exacta (puede en la misma calle, pero no exacta, es decir, el string entero con el numero de la calle)
        UsuarioRepetido = Perfil_Privado.objects.filter(usuarios=usuarios).first()
        if(not UsuarioRepetido is None
           ):
             if(not self.instance is None and UsuarioRepetido.id == self.instance.id):
                 pass
             else:
                self.add_error('usuarios','Este usuario ya tiene un perfil publico')
        
        return self.cleaned_data
