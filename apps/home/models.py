from auditlog.registry import auditlog
from django.db import models
from django.contrib.auth.models import User
from django.apps import apps
from datetime import date

from django.core.validators import MaxValueValidator, MinValueValidator




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
    

        
        
class Semana(models.Model):
    id = models.AutoField(primary_key = True, null=False)
    dia = models.CharField(max_length = 10, blank = False, null = False)
    numero = models.IntegerField(primary_key = False, null=True, blank = True)
    
    class Meta:
        verbose_name = 'Semana'
        verbose_name_plural = 'Semana'
        ordering = ['numero']
        
    def __str__(self):
        return self.dia




    
class Alumno(models.Model):
    id = models.AutoField(primary_key = True, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length = 60, blank = False, null = True, verbose_name="Nombre")
    apellido = models.CharField(max_length = 60, blank = False, null = True)
    fecha_nac = models.DateField(blank = False, null = True)
    email = models.EmailField(max_length = 70, blank = False, null = False)
    estado = models.BooleanField(default=True)
    entrenamiento_sistema = models.BooleanField(default=None, null=True)
    rutina_id = models.ForeignKey('rutina.Rutina', related_name='rutina', on_delete=models.CASCADE, verbose_name="Rutina", blank=True, null=True)
    profesor_id = models.ForeignKey(Profesor, on_delete=models.CASCADE, verbose_name="Profesor")
    nivel_id = models.ForeignKey('rutina.Nivel', related_name='rutina', on_delete=models.CASCADE, verbose_name="Nivel", null=True, blank=True)
    semana_id = models.ManyToManyField(Semana, verbose_name="Dias", blank=True)
    fechaCambioEntrenamiento = models.DateField(blank = True, null = True, verbose_name="Fecha de cambio de entrenamiento")
    
    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre + ', ' + self.apellido
    
    def edad(self, fecha_nac):
        diferencia_fechas = date.today() - fecha_nac
        diferencia_fechas_dias = diferencia_fechas.days
        edad_numerica = diferencia_fechas_dias / 365.2425
        edad = int(edad_numerica)
        return edad

    
    
class DisponibilidadProfesor(models.Model):
    id = models.AutoField(primary_key = True, null=False)
    horario_inicio = models.TimeField(blank = False, null = True)
    horario_final = models.TimeField(blank = False, null = True)
    ocupado = models.BooleanField(default=False)
    estado = models.BooleanField(default=True)
    semana_id = models.ForeignKey(Semana, on_delete=models.CASCADE, verbose_name="Dia")
    profesor_id = models.ForeignKey(Profesor, on_delete=models.CASCADE, verbose_name="Profesor")
    alumno_id = models.ForeignKey(Alumno, on_delete=models.SET_NULL, verbose_name="Alumno", null=True, blank=True)
    
    
    class Meta:
        verbose_name = 'Disponibilidad Profesor'
        verbose_name_plural = 'Disponibilidad Profesor'
        ordering = ['horario_inicio']
        
    def __str__(self):

        return str(self.semana_id) + ' (' + str(self.horario_inicio) + ' - ' + str(self.horario_final)+'hs)'
    
    
        

class FichaAlumno (models.Model):
    id = models.AutoField(primary_key=True, null=False)
    peso = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=False, validators=[
            MaxValueValidator(400),
            MinValueValidator(20)
        ])
    sexo = models.CharField(max_length = 1, blank = False, null = True)
    altura = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=False, validators=[
            MinValueValidator(1),
            MaxValueValidator(3),
        ])
    grupo_sanguineo = models.CharField(max_length = 2, blank = False, null = False)
    circunferenciaMuneca = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[
            MinValueValidator(5),
            MaxValueValidator(200),
        ])
    profesion = models.CharField(max_length = 40, blank = False, null = True)
    alumno_id = models.OneToOneField(Alumno, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Ficha'
        verbose_name_plural = 'Fichas'
        ordering = ['alumno_id']
    
    def __str__(self):
        return 'Ficha '+self.alumno_id.nombre



class Auditoria (models.Model):
    id = models.AutoField(primary_key=True, null=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length = 60, blank = False, null = False)
    calle = models.CharField(max_length = 30, blank = False, null = False)
    altura = models.IntegerField(primary_key = False, null=False, blank = False)
    ciudad = models.CharField(max_length = 30, blank = False, null = False)
    provincia = models.CharField(max_length = 30, blank = False, null = False)
    telefono = models.CharField(max_length = 10, blank = False, null = False)
    
    class Meta:
        verbose_name = 'Auditoria'
        verbose_name_plural = 'Auditorias'
        ordering = ['user']
    
    def __str__(self):
        return 'Configuracion '+str(self.user)
