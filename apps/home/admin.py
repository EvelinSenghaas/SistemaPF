from django.contrib import admin
from .models import Profesor, Alumno, FichaAlumno, Semana, DisponibilidadProfesor

# Register your models here.
admin.site.register(Profesor)
admin.site.register(Alumno)
admin.site.register(FichaAlumno)
admin.site.register(Semana)
admin.site.register(DisponibilidadProfesor)