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
    email = models.EmailField(max_length = 70, blank = False, null = False)
    sexo = models.CharField(max_length = 1, blank = False, null = True)
    estado = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Profesor'
        verbose_name_plural = 'Profesores'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
class Alumno(models.Model):
    id = models.AutoField(primary_key = True, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length = 60, blank = False, null = True)
    apellido = models.CharField(max_length = 60, blank = False, null = True)
    fecha_nac = models.DateField(blank = False, null = True)
    email = models.EmailField(max_length = 70, blank = False, null = True)
    estado = models.BooleanField(default=True)
    rutina_id = models.ForeignKey('rutina.Rutina', related_name='rutina', on_delete=models.CASCADE, verbose_name="Rutina")
    profesor_id = models.ForeignKey(Profesor, on_delete=models.CASCADE, verbose_name="Profesor")
    
    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre

class FichaAlumno (models.Model):
    id = models.AutoField(primary_key=True, null=False)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=False)
    sexo = models.CharField(max_length = 1, blank = False, null = True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=False)
    grupo_sanguineo = models.CharField(max_length = 2, blank = False, null = False)
    profesion = models.CharField(max_length = 40, blank = False, null = True)
    alumno_id = models.OneToOneField(Alumno, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Ficha'
        verbose_name_plural = 'Fichas'
        ordering = ['alumno_id']
    
    def __str__(self):
        return 'Ficha '+self.alumno_id.nombre

    
    