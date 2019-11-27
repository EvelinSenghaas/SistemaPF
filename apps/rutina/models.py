from auditlog.registry import auditlog
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
    profesor_id = models.ForeignKey('home.Profesor', related_name='homeEN', on_delete=models.CASCADE, null=True, blank=True)
    
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
    gif = models.ImageField(upload_to="gif_actividad", null=True, blank=True)
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
    
class Sesion(models.Model):
    id = models.AutoField(primary_key = True)
    alumno_id = models.ForeignKey('home.Alumno', related_name='homeAS', on_delete=models.CASCADE)
    fechaSesion = models.DateField(blank = True, null = True, verbose_name="Fecha de la sesion")
    actividad_id = models.ManyToManyField(Actividad, verbose_name="Actividad", blank=True, null=True)
    rutina_id = models.ForeignKey(Rutina, verbose_name="Rutina", on_delete=models.CASCADE)
    profesor_id = models.ForeignKey('home.Profesor', related_name='homePS', on_delete=models.CASCADE)
    #agregar los dos atributos que faltan
    cantSesiones = models.IntegerField(blank = True, null = True, verbose_name="Sesiones parciales")
    sesionesRealizadas = models.IntegerField(blank = True, null = True, verbose_name="Sesiones totales")
    esfuerzoSesion = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    descripcion = models.TextField(blank = True, null = True)
    claseRevision = models.BooleanField(default=False, verbose_name="Clase de revision")
    
    
    
    class Meta:
        verbose_name = 'Sesion'
        verbose_name_plural = 'Sesiones'
        ordering = ['fechaSesion']
        get_latest_by = "fechaSesion"
    
    def __str__ (self):
        return self.alumno_id.nombre + ' '+self.alumno_id.apellido+ ' (' + str(self.fechaSesion)+ ')'
    
class EsfuerzoActividad(models.Model):
    id = models.AutoField(primary_key = True)
    alumno_id = models.ForeignKey('home.Alumno', related_name='homeASEA', on_delete=models.CASCADE)
    esfuerzoActividad = models.IntegerField(blank = True, null = True, verbose_name="Costo de actividad")
    actividad_id = models.ForeignKey(Actividad, on_delete=models.CASCADE, verbose_name="Actividad")
    sesion_id = models.ForeignKey(Sesion, on_delete=models.CASCADE)
    nombreActividad =  models.CharField(max_length = 60, blank = True, null = True)
    nivel_id = models.CharField(max_length = 60, blank = True, null = True, verbose_name="Nivel de sesion")
    
    class Meta:
        verbose_name = 'Esfuerzo de actividad'
        verbose_name_plural = 'Esfuerzos de actividades'
        ordering = ['id']
    
    def __str__ (self):
        return self.actividad_id.nombre +' '+ str(self.esfuerzoActividad)
    
    
class Revision(models.Model):
    id = models.AutoField(primary_key = True)
    fechaRevision = models.DateField('Fecha de creacion', auto_now = True, auto_now_add = False)
    profesor_id = models.ForeignKey('home.Profesor', related_name='homePR', on_delete=models.CASCADE)
    sesion_id = models.ForeignKey(Sesion, on_delete=models.CASCADE)
    
    
    class Meta:
        verbose_name = 'Revision'
        verbose_name_plural = 'Revisiones'
        ordering = ['fechaRevision']
        get_latest_by = "fechaRevision"
    
    def __str__ (self):
        return self.sesion_id.alumno_id.nombre + ', ' + self.sesion_id.alumno_id.apellido  + ' (' + str(self.fechaRevision) + ' )'


class RevisionSesion(models.Model):
    id = models.AutoField(primary_key = True)
    fechaRevision = models.DateField('Fecha de revision', auto_now = True, auto_now_add = False, blank=True, null=True)
    profesor_id = models.ForeignKey('home.Profesor', related_name='homePRS', on_delete=models.CASCADE)
    alumno_id = models.ForeignKey('home.Alumno', related_name='homeARS', on_delete=models.CASCADE)
    sesion_id = models.ForeignKey(Sesion, on_delete=models.CASCADE)
    nivelAnterior = models.CharField(max_length = 60, blank = False, null = False, unique=True, verbose_name="Nivel anterior")
    nivelRevision = models.CharField(max_length = 60, blank = False, null = False, unique=True, verbose_name="Nivel revision")
    pesoActual = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Peso anterior")
    pesoRevision = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Peso revision")
    revisado = models.BooleanField(default=False)
    comentario = models.TextField(blank = True, null = True)
    
    class Meta:
        verbose_name = 'Revision de sesion'
        verbose_name_plural = 'Revisiones de sesion'
        ordering = ['fechaRevision']
        get_latest_by = "fechaRevision"
    
    def __str__ (self):
        return self.sesion_id.alumno_id.nombre + ', ' + self.sesion_id.alumno_id.apellido  + ' (' + str(self.fechaRevision) + ' )'
    
    
