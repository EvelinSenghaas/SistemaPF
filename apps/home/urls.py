from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import registro, Home, cargarDatosUsuario, Administrar, listadoAlumnos, agregarDisponibilidad, reporte, listadoDisponibilidad, editarDisponibilidad

urlpatterns = [
    path('', login_required(Home.as_view()), name = 'index'),
    path('administracion/', login_required(Administrar.as_view()), name = 'index'),
    path('cargar_datos/', cargarDatosUsuario, name='cargar_datos'),
    path('listado_alumnos/<int:pk>', login_required(listadoAlumnos), name='listado_alumnos'),
    path('agregar_disponibilidad/<int:pk>', login_required(agregarDisponibilidad), name='agregar_disponibilidad'),
    path('generar_pdf/<alumnos>', login_required(reporte), name='generar_pdf'),
    path('administrar_disponibilidad/<int:pk>', login_required(listadoDisponibilidad), name='administrar_disponibilidad'),
    path('editar_disponibilidad/<int:pk>', login_required(editarDisponibilidad), name='editar_disponibilidad'),
]