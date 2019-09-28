from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import Rutinas, ListadoDetalles, ListadoRutinas, ListadoActividades, EditarRutina, editarActividad, EditarDetalle, EliminarActividad, AgregarRutina, AgregarDetalle, agregarActividad, EliminarRutina, EliminarDetalle, verRutina, verActividad, agregarRutina, inscribirseRutina, perfil, verClase

urlpatterns = [
    path('',  login_required(ListadoRutinas.as_view()), name = 'rutinas'),
    path('actividades/',  login_required(ListadoActividades.as_view()), name = 'actividades'),
    
    path('agregar_detalle',login_required(AgregarDetalle.as_view(success_url="/rutinas/administrar_detalles/")), name = 'agregar_detalle'),
    path('editar_detalle/<int:pk>', login_required(EditarDetalle.as_view(success_url="/rutinas/administrar_detalles/")), name='editar_detalle'),
    path('administrar_detalles/', login_required(ListadoDetalles.as_view()), name='administrar_detalles/'),
    path('eliminar_detalle/<int:pk>', login_required(EliminarDetalle.as_view(success_url="/rutinas/administrar_detalles/")), name='eliminar_detalle'), 
    
    path('agregar_actividad',login_required(agregarActividad), name = 'agregar_actividad'),
    path('editar_actividad/<int:pk>', login_required(editarActividad), name='editar_actividad'),
    path('eliminar_actividad/<int:pk>', login_required(EliminarActividad.as_view(success_url="/rutinas/actividades")), name='eliminar_actividad'), 
    path('ver_actividad/<int:pk>', login_required(verActividad), name='ver_actividad'),
    
    path('agregar_rutina/<int:pk>',login_required(agregarRutina), name = 'agregar_rutina'),
    path('editar_rutina/<int:pk>', login_required(EditarRutina.as_view(success_url="/rutinas/administrar_rutinas/")), name='editar_rutina'),
    path('eliminar_rutina/<int:pk>', login_required(EliminarRutina.as_view(success_url="/rutinas/administrar_rutinas/")), name='eliminar_rutina'),    
    path('ver_rutina/<int:pk>', login_required(verRutina), name='ver_rutina'),
    path('administrar_rutinas/', login_required(Rutinas.as_view()), name='administrar_rutinas/'),
    
    path('inscribir_rutina/<int:pk1>/<int:pk2>', login_required(inscribirseRutina), name='inscribir_rutina/'), 
    
    path('ver_perfil/<int:pk>', login_required(perfil), name='ver_perfil'),
    
    path('clases/<int:pk>', login_required(verClase), name='clases'),
    
    
    
    
    
]