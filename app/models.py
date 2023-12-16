from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator,MinLengthValidator


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
    
    def __str__(self):
        return self.nombre
    

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
        default=1
     )
    
    deporte = models.ForeignKey(Deportes, verbose_name=("deporte"), on_delete=models.CASCADE)
    usuario_valoracion = models.ManyToManyField(Usuarios, through="Votacion", related_name="votacion_usuario")   
    usurio = models.ManyToManyField(Usuarios, through="Rel_Usu_Equi", related_name="usuario_equipo")   
    
#Necesito validar el numero maximo de jugadores en funcion al deporte


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=150)
    capacidad = models.IntegerField()
    calle = models.CharField(max_length=150)
    
    equipo = models.ManyToManyField(Equipos, verbose_name=("equipo"))
    
    deporte = models.ManyToManyField(Deportes, verbose_name=("deporte"))


class Detalles_Ubicacion(models.Model):
    ubicacion  = models.OneToOneField(Ubicacion, verbose_name=("ubicacion"), on_delete=models.CASCADE)
    incidentes = models.BooleanField()
    cubierto = models.BooleanField()



class Perfil_Publico(models.Model):
    descripcion = models.TextField()
    lugar_fav = models.ForeignKey(Ubicacion, verbose_name=("lugar_fav"), on_delete=models.CASCADE)
    deportes_fav = models.TextField()
    hitos_publicos = models.TextField()
    #me faltaba la relacion con usuarios
    usuarios = models.OneToOneField(Usuarios, on_delete=models.CASCADE)
    
#lugar_fav y deportes_fav deberia ser una lista elegible de Ubicacion y Deportes respectivamente
    
    
class Perfil_Privado(models.Model):
    historial_trayectoria = models.TextField()
    incidencias = models.TextField()
    hitos = models.TextField() 
    usuarios = models.OneToOneField(Usuarios, on_delete=models.CASCADE) 
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

class Votacion(models.Model):
    puntuacion = models.IntegerField(default=0)
    comentario = models.CharField(max_length=400)
    fecha = models.DateTimeField(default=timezone.now)
    
    usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    equipos = models.ForeignKey(Equipos, on_delete=models.CASCADE)
    

class CuentaBancaria(models.Model):
    BANCOS = [('Caixa','Caixa'), 
              ('BBVA','BBVA'), 
              ('UNICAJA','UNICAJA'),
              ('ING','ING')]
    
    nombre = models.CharField(
        choices=BANCOS,
        max_length=10
        
    )
    
    
    numero_cuenta  = models.IntegerField()
    
    usuario = models.OneToOneField(Usuarios, on_delete=models.CASCADE)
    
    
class Promocion(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.CharField(
        max_length=400,
        validators=[MinLengthValidator(limit_value=100)])
        
    descuento = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    fecha_fin_promocion = models.DateTimeField(
        validators=[MinValueValidator(limit_value=timezone.now())])
    
    usuarios = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    