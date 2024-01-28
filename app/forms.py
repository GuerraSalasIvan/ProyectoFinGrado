from django.forms import ModelForm
from django import forms
from .models import *
from datetime import date
import datetime
from django.contrib.auth.forms import UserCreationForm

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
    textoBusqueda = forms.CharField(required=True)
    


class BusquedaAvanzadaEquipoForm(forms.Form):
    
    textoBusqueda = forms.CharField(required=False)
    capacidad = forms.IntegerField(required=False)

    def clean(self):
        super().clean()
        
        #Obtenemos los campos
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        capacidad = self.cleaned_data.get('capacidad')

        if(textoBusqueda == ""):
             self.add_error('textoBusqueda', 'no textoBusqueda')
        
        if(capacidad == ""
           or capacidad < 0):
             self.add_error('capacidad', 'no capacidad')
        
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
        fields = ['edad','sexo']
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
    

class BusquedaAvanzadaUsuarioForm(forms.Form):
    
    #creamos el formulario
    textoBusqueda = forms.CharField(required=False)
    rangoEdad = forms.IntegerField(required=False)
    sexo = forms.ChoiceField(choices=Usuarios.GENERO, required=False)
    
    def clean(self):
        super().clean()
        
        #Obtenemos los campos
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        rangoEdad = self.cleaned_data.get('rangoEdad')
        sexo = self.cleaned_data.get('sexo')
        
        #al menos tiene que poner un campo
        if(textoBusqueda == ""
           and rangoEdad is None
           and sexo is None):
             self.add_error('textoBusqueda', 'no textoBusqueda')
             self.add_error('rangoEdad', 'no rangoEdad')
             self.add_error('sexo', 'no hay usuarios')
             
              #solo permitir buscar por edad menor a 100 años
        else:
            if (not(rangoEdad is None) and (rangoEdad < 0 and rangoEdad > 100)):
                self.add_error('rangoEdad', 'debe ser mayor que 0 y menor a 100')
    

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
    
class BusquedaAvanzadaUbicacionForm(forms.Form):
    
    equiposdisponibles = Equipos.objects.all()
    deportesdisponibles = Deportes.objects.all()
    
    
    #creamos el formulario
    textoBusqueda = forms.CharField(required=False)
    capacidad = forms.IntegerField(required=False)
    equipo = forms.ModelMultipleChoiceField(queryset=equiposdisponibles, widget=forms.SelectMultiple, required=False)
    deporte = forms.ModelMultipleChoiceField(queryset=deportesdisponibles, widget=forms.SelectMultiple, required=False)
    
    
    def clean(self):
        super().clean()
        
        #Obtenemos los campos
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        capacidad = self.cleaned_data.get('capacidad')
        calle = self.cleaned_data.get('calle')
        equipo = self.cleaned_data.get('equipo')
        deporte = self.cleaned_data.get('deporte')
        
        #al menos tiene que poner un campo
        if(textoBusqueda == ""
           and capacidad is None
           and len(equipo) == 0
           and len(deporte) == 0):
             self.add_error('textoBusqueda', 'no textoBusqueda')
             self.add_error('capacidad', 'no capacidad')
             self.add_error('equipo', 'no hay equipo')
             self.add_error('deporte', 'no hay deporte')
             

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
    
class BusquedaAvanzadaPerfilPublicoForm(forms.Form):
    
    ubicaciondisponibles = Ubicacion.objects.all()
    usuariosdisponibles = Usuarios.objects.all()

    #creamos el formulario
    descripcion = forms.CharField(required=False)
    hitos_publicos = forms.CharField(required=False)

    usuarios = forms.ModelMultipleChoiceField(queryset=usuariosdisponibles, widget=forms.SelectMultiple, required=False)
    lugar_fav = forms.ModelMultipleChoiceField(queryset=ubicaciondisponibles, widget=forms.SelectMultiple, required=False)
    

    def clean(self):
        super().clean()
        
        #Obtenemos los campos
        descripcion = self.cleaned_data.get('descripcion')
        hitos_publicos = self.cleaned_data.get('hitos_publicos')
        usuarios = self.cleaned_data.get('usuarios')
        lugar_fav = self.cleaned_data.get('lugar_fav')
        
        #al menos tiene que poner un campo
        if(descripcion == ""
           and hitos_publicos == ""
           and len(usuarios) == 0
           and len(lugar_fav) == 0):
             self.add_error('descripcion', 'no descripcion')
             self.add_error('hitos_publicos', 'no hitos_publicos')
             self.add_error('usuarios', 'no hay usuarios')
             self.add_error('lugar_fav', 'no hay lugar_fav')
             
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
    
    
class BusquedaAvanzadaPerfilPrivadoForm(forms.Form):
    
    usuariosdisponibles = Usuarios.objects.all()

    #creamos el formulario
    incidencias = forms.CharField(required=False)
    usuarios = forms.ModelMultipleChoiceField(queryset=usuariosdisponibles, widget=forms.SelectMultiple, required=False)
    

    def clean(self):
        super().clean()
        
        #Obtenemos los campos
        incidencias = self.cleaned_data.get('incidencias')
        usuarios = self.cleaned_data.get('usuarios')
        
        #al menos tiene que poner un campo
        if(incidencias == ""
           and len(usuarios) == 0):
             self.add_error('incidencias', 'no incidencias')
             self.add_error('usuarios', 'no hay usuarios')
             
        return self.cleaned_data
    
    
class RegistroForm(UserCreationForm):
    
    roles = (
        (UserLogin.cliente, 'cliente'),
        (UserLogin.entrenador, 'entrenador')
    )
    
    rol = forms.ChoiceField(choices=roles)
    
    class Meta:
        model = UserLogin
        fields = ('username','email','password1','password2','rol')
        