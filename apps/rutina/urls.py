from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import Rutinas, ListadoRutinas, EditarRutina, AgregarRutina, AgregarDetalle, AgregarActividad, EliminarRutina, verRutina

urlpatterns = [
    path('',  login_required(ListadoRutinas.as_view()), name = 'rutinas'),
    path('agregar_detalle',login_required(AgregarDetalle.as_view(success_url="/rutinas/")), name = 'agregar_detalle'),
    path('agregar_actividad',login_required(AgregarActividad.as_view(success_url="/rutinas/")), name = 'agregar_actividad'),
    path('agregar_rutina',login_required(AgregarRutina.as_view(success_url="/rutinas/")), name = 'agregar_rutina'),
    path('editar_rutina/<int:pk>', login_required(EditarRutina.as_view(success_url="/rutinas/")), name='editar_rutina'),
    path('eliminar_rutina/<int:pk>', login_required(EliminarRutina.as_view(success_url="/rutinas/")), name='eliminar_rutina'),    
    path('ver_rutina/<int:pk>', login_required(verRutina), name='ver_rutina'),
]