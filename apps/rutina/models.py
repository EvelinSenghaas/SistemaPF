from django.db import models
from django.db.models import *



# Create your models here.
class Detalle(models.Model):
    id = models.AutoField(primary_key = True)
    categoria = models.CharField(max_length = 30, blank = False, null = False)
    musculo = models.CharField(max_length = 30, blank = False, null = False, unique=True)
    estado = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Detalle'
        verbose_name_plural = 'Detalles'
        ordering = ['categoria']
    
    def __str__ (self):
        return self.musculo
    
    def obtenerId(self):
        return self.id
    
class Nivel(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60, blank = False, null = False, unique=True)
    class Meta:
        verbose_name = 'Nivel'
        verbose_name_plural = 'Niveles'
        ordering = ['nombre']
        
    def __str__ (self):
        return self.nombre
    
    def nivel(self):
        return self.nombre
    
class EvaluacionNivel(models.Model):
    id = models.AutoField(primary_key = True)
    nivel_id = models.ForeignKey(Nivel, on_delete=models.CASCADE, verbose_name="Nivel")
    cantSesiones = models.PositiveIntegerField(blank=False, null=False, verbose_name="Sesiones Minimas")
    profesor_id = models.ForeignKey('home.Profesor', related_name='homeEN', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Evaluacion de nivel'
        verbose_name_plural = 'Evaluaciones de nivel'
        ordering = ['nivel_id']
    
    def __str__ (self):
        return str(self.nivel_id.nombre) + ' ' + str(self.cantSesiones) + ' sesiones ('+ self.profesor_id.nombre + ')'
    

class Actividad(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60, blank = False, null = False, unique=True)
    descripcion = models.TextField(blank = False, null = True)
    detalle_id = models.ManyToManyField(Detalle, verbose_name="Detalle")
    estado = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['nombre']
    
    def __str__ (self):
        return self.nombre
    
class Repeticion(models.Model):
    id = models.AutoField(primary_key = True)
    actividad_id = models.ForeignKey(Actividad, on_delete=models.CASCADE, verbose_name="Actividad")
    nivel_id = models.ForeignKey(Nivel, on_delete=models.CASCADE, verbose_name="Nivel")
    repeticionesMinimas = models.PositiveIntegerField(blank=False, null=False, verbose_name="Repeticiones Minimas")
    class Meta:
        verbose_name = 'Repeticion'
        verbose_name_plural = 'Repeticiones'
        ordering = ['id']
        
    def __str__ (self):
        return self.actividad_id.nombre + ' ' + self.nivel_id.nombre
    
class Rutina(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60, blank = False, null = False, unique=True, verbose_name="Nombre")
    descripcion = models.TextField(blank = False, null = False)
    estado = models.BooleanField(default=True)
    actividad_id = models.ManyToManyField(Actividad, verbose_name="Actividad")
    profesor_id = models.ForeignKey('home.Profesor', related_name='home', on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Rutina'
        verbose_name_plural = 'Rutinas'
        ordering = ['nombre']
    
    def __str__ (self):
        return self.nombre
    
    def id(self):
        return self.id
    
