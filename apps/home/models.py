from django.db import models


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
    
    