from django.contrib import admin
from .models import Rutina, Actividad, Detalle, Nivel, Repeticion

# Register your models here.
admin.site.register(Rutina)
admin.site.register(Actividad)
admin.site.register(Detalle)
admin.site.register(Nivel)
admin.site.register(Repeticion)