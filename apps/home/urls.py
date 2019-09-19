from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import registro, Home, cargarDatosUsuario, Administrar, listadoAlumnos

urlpatterns = [
    path('', login_required(Home.as_view()), name = 'index'),
    path('administracion/', login_required(Administrar.as_view()), name = 'index'),
    path('cargar_datos/', cargarDatosUsuario, name='cargar_datos'),
    path('listado_alumnos/<int:pk>', login_required(listadoAlumnos), name='listado_alumnos')
    #path('registro',registro, name = 'registro')
]