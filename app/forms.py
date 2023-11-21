from django.forms import ModelForm
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
            
   