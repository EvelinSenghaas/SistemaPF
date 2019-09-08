from django.db import models
from django.contrib.auth.models import User
from django.apps import apps




# Create your models here.
class Usuario(models.Model):
    id = models.AutoField(primary_key = True)
    
    username = models.CharField(max_length = 60, blank = False, null = False, unique=True )
    password = models.CharField(max_length = 20, blank = False, null = False)
    email = models.EmailField(max_length = 70, blank = False, null = False)
    #fechaCreacion = models.DateField('Fecha de creacion', auto_now = True, auto_now_add = False)
    
    #Datos generales
    nombres= models.CharField(max_length = 70, blank = False, null = False)
    apellidos= models.CharField(max_length = 60, blank = False, null = False)
    fechaNac = models.DateField('Fecha de nacimiento', blank = True, null = True)
    sexo = models.CharField(max_length = 1, blank = False, null = False)
    nacionalidad = models.CharField(max_length = 25, blank = False, null = False)
    
    #Datos especiales
    altura = models.DecimalField(max_digits=2, decimal_places=2,)
    peso =   models.DecimalField(max_digits=3, decimal_places=3,)
    
    
    

class Profesor(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length = 60, blank = False, null = True)
    apellido = models.CharField(max_length = 60, blank = False, null = True)
    fecha_nac = models.DateField(blank = False, null = True)
    sexo = models.CharField(max_length = 1, blank = False, null = True)
    """class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
        ordering = ['nombre']"""
    
    def __str__(self):
        return self.nombre
    
class Alumno(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length = 60, blank = False, null = True)
    apellido = models.CharField(max_length = 60, blank = False, null = True)
    fecha_nac = models.DateField(blank = False, null = True)
    sexo = models.CharField(max_length = 1, blank = False, null = True)
    rutina_id = models.ForeignKey('rutina.Rutina', related_name='rutina', on_delete=models.CASCADE, verbose_name="Rutina", null = True)
    
    """class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['nombre']"""
    
    def __str__(self):
        return self.nombre
    

    
    