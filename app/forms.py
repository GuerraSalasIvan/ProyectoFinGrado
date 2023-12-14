from django.forms import ModelForm
from django import forms
from .models import *
from datetime import date
import datetime


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
        
    
    
'''

    deporte = forms.MultipleChoiceField(choices=Equipos.deporte, required=False, widget=forms.CheckboxSelectMultiple())
    
    usuario = forms.MultipleChoiceField(choices=Equipos.usurio, required=False, widget=forms.CheckboxSelectMultiple())
    
    capacidad = forms.MultipleChoiceField(range(1,20))
    

    def clean(self):
        super().clean()
        
        #Obtenemos los campos
        textoBusqueda = self.cleaned_data.get('textoBusqueda')
        deporte = self.cleaned_data.get('deporte')
        usuario = self.cleaned_data.get('usuario')
        capacidad  = self.cleaned_data.get('capacidad')
    
        #controlar campos
        if(textoBusqueda == ""
            and len(deporte) == 0
            and len(usuario) == 0
            and capacidad == 0
        ):
            self.add_error('textoBusqueda', 'no textoBusqueda')
            self.add_error('deporte', 'no deporte')
            self.add_error('usuario', 'no usuario')
            self.add_error('capacidad', 'no capacidad')
            
        return self.cleaned_data
'''