from django.db import models

# Create your models here.
class Rutina(models.Model):
    id = models.AutoField(primary_key = True)
    nombre = models.CharField(max_length = 50, blank = False, null = False)
    descripcion = models.TextField(blank = False, null = False)


