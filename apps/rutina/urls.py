from django.urls import path, re_path
from .views import Rutinas, agregarDetalle, agregarActividad, agregarRutina

urlpatterns = [
    path('', Rutinas, name = 'rutinas'),


    path('agregar_detalle',agregarDetalle, name = 'agregar_detalle'),
    path('agregar_actividad',agregarActividad, name = 'agregar_actividad'),
    path('agregar_rutina',agregarRutina, name = 'agregar_actividad'),    
]