from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Usuarios(models.Model):
    nombre = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=150)
    edad = models.IntegerField()
    GENERO = [
        ('MAS','Masculino'),
        ('FEM','Femenino'),
        ('---','Sin_Asignar'),
    ]
    #Si no se especifica el género, no se puede participar en deportes.
    sexo = models.CharField(
        max_length = 3,
        choices= GENERO,
        default = '---'
    )
    

class Categoria_Persona(models.Model):
    CATEGORIA = [
        ('BEN','Benjamin'),
        ('INF','Infatil'),
        ('ALE','Alevin'),
        ('CAD','Cadete'),
        ('JUN','Junior'),
        ('SEN','Senior'),
    ]
    #La categoria deberia calcularse sola en funcion a la edad del jugador
    sexo = models.CharField(
        max_length = 3,
        choices= CATEGORIA,
        default = 'SEN'
    )
    
    usuario = models.ForeignKey(Usuarios, verbose_name=("usuario"), on_delete=models.CASCADE)  
#la categoria se asigna automaticamente segun la edad  
    
    
class Deportes(models.Model):
    DEPORTES = [
        ('FUT','Futbol'),
        ('BSK','Baloncesto'),
        ('PDL','Padel'),
        ('---','Sin_Asignar'),
    ]
    
    deporte = models.CharField(
        max_length = 3,
        choices= DEPORTES,
        default = '---'
    )



class Equipos(models.Model):
    nombre = models.CharField(max_length=60)
    capacidad = models.IntegerField(
        default=1,
        validators=[
            MaxValueValidator(20),
            MinValueValidator(1)
        ]
     )
    
    deporte = models.ForeignKey(Deportes, verbose_name=("deporte"), on_delete=models.CASCADE)
    
    usurio = models.ManyToManyField(Usuarios, through="Rel_Usu_Equi", related_name="usuario_equipo")   
#Necesito validar el numero maximo de jugadores en funcion al deporte


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=150)
    capacidad = models.IntegerField()
    calle = models.CharField(max_length=150)
    
    equipo = models.ManyToManyField(Equipos, verbose_name=("equipo"))
    
    deporte = models.ManyToManyField(Deportes, verbose_name=("deporte"))


class Detalles_Ubicacion(models.Model):
    models.OneToOneField(Ubicacion, verbose_name=("ubicacion"), on_delete=models.CASCADE)
    incidentes = models.BooleanField()
    cubierto = models.BooleanField()



class Perfil_Publico(models.Model):
    descripcion = models.TextField()
    lugar_fav = models.ForeignKey(Ubicacion, verbose_name=("lugar_fav"), on_delete=models.CASCADE)
    deportes_fav = models.TextField()
    hitos_publicos = models.TextField()
#lugar_fav y deportes_fav deberia ser una lista elegible de Ubicacion y Deportes respectivamente
    
    
class Perfil_Privado(models.Model):
    historial_trayectoria = models.TextField()
    incidencias = models.TextField()
    hitos = models.TextField()  
#En hitos se debe guardar todas las hazañas del jugador, llega a x división x año, entra en x equipo, juega durante x tiempo en x equipo, y hitos_publicos el jugadore decide que hitos hacer públicos.


class Rel_Usu_Equi(models.Model):
    usuario = models.ForeignKey(Usuarios, verbose_name=("usuario"), on_delete=models.CASCADE)
    
    equipos = models.ForeignKey(Equipos, verbose_name=("equipos"), on_delete=models.CASCADE) 
    
    
class Rel_Equi_Ubi(models.Model):
    ubicacion = models.ForeignKey(Ubicacion, verbose_name=("ubicacion"), on_delete=models.CASCADE)
    
    equipos = models.ForeignKey(Equipos, verbose_name=("equipos"), on_delete=models.CASCADE) 


class Rel_Dep_Ubi(models.Model):
    deporte = models.ForeignKey(Deportes, verbose_name=("deporte"), on_delete=models.CASCADE)
    
    equipos = models.ForeignKey(Equipos, verbose_name=("equipos"), on_delete=models.CASCADE) 
