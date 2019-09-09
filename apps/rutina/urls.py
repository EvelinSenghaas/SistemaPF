from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import Rutinas, ListadoRutinas, ListadoActividades, EditarRutina, EditarActividad, EliminarActividad, AgregarRutina, AgregarDetalle, AgregarActividad, EliminarRutina, verRutina, agregarRutina

urlpatterns = [
    path('',  login_required(ListadoRutinas.as_view()), name = 'rutinas'),
    path('actividades/',  login_required(ListadoActividades.as_view()), name = 'actividades'),
    
    path('agregar_detalle',login_required(AgregarDetalle.as_view()), name = 'agregar_detalle'),
    path('agregar_actividad',login_required(AgregarActividad.as_view(success_url="/rutinas/actividades/")), name = 'agregar_actividad'),
    path('editar_actividad/<int:pk>', login_required(EditarActividad.as_view(success_url="/rutinas/actividades")), name='editar_actividad'),
    path('eliminar_actividad/<int:pk>', login_required(EliminarActividad.as_view(success_url="/rutinas/actividades")), name='eliminar_actividad'), 
    
    path('agregar_rutina/<int:pk>',login_required(agregarRutina), name = 'agregar_rutina'),
    path('editar_rutina/<int:pk>', login_required(EditarRutina.as_view(success_url="/rutinas/administrar_rutinas/")), name='editar_rutina'),
    path('eliminar_rutina/<int:pk>', login_required(EliminarRutina.as_view(success_url="/rutinas/administrar_rutinas/")), name='eliminar_rutina'),    
    path('ver_rutina/<int:pk>', login_required(verRutina), name='ver_rutina'),
    path('administrar_rutinas/', login_required(Rutinas.as_view()), name='administrar_rutinas/'),
]