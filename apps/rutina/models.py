from django.db import models

# Create your models here.
class Rutina(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60, blank = False, null = False)
    descripcion = models.TextField(blank = False, null = False)
    actividad_id = models.ManyToManyField(Actividad)
    class Meta:
        verbose_name = 'Rutina'
        verbose_name_plural = 'Rutinas'
        ordering = ['nombre']
    
    def __str__ (self):
        return self.nombre
    
    
class Actividad(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60, blank = False, null = False)
    descripcion = models.TextField(blank = False, null = False)
    rutina_id = models.ManyToManyField(Rutina)
    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['nombre']
    
    def __str__ (self):
        return self.nombre
    