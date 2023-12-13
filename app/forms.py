from django.forms import ModelForm
from django import forms
from .models import *

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