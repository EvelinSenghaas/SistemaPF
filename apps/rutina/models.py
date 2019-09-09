from django.db import models



# Create your models here.
class Detalle(models.Model):
    id = models.AutoField(primary_key = True)
    categoria = models.CharField(max_length = 30, blank = False, null = True)
    musculo = models.CharField(max_length = 30, blank = False, null = True)
    class Meta:
        verbose_name = 'Detalle'
        verbose_name_plural = 'Detalles'
        ordering = ['categoria']
    
    def __str__ (self):
        return self.atributo
    


class Actividad(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60, blank = False, null = True)
    descripcion = models.TextField(blank = False, null = True)
    detalle_id = models.ManyToManyField(Detalle, verbose_name="Detalle")
    estado = models.BooleanField(default=True)
    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'
        ordering = ['nombre']
        permissions = (
            
        )
    
    def __str__ (self):
        return self.nombre
    

class Rutina(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 60, blank = False, null = True)
    descripcion = models.TextField(blank = False, null = True)
    estado = models.BooleanField(default=True)
    actividad_id = models.ManyToManyField(Actividad, verbose_name="Actividad")
    profesor_id = models.ForeignKey('home.Profesor', related_name='home', on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'Rutina'
        verbose_name_plural = 'Rutinas'
        ordering = ['nombre']
    
    def __str__ (self):
        return self.nombre
    
    def asociarProfesor(self, pk):
        self.profesor_id=pk
