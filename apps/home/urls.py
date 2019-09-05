from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import registro, Home, cargarDatosUsuario, Administrar

urlpatterns = [
    path('', login_required(Home.as_view()), name = 'index'),
    path('administracion/', login_required(Administrar.as_view()), name = 'index'),
    path('cargar_datos/', cargarDatosUsuario, name='cargar_datos'),
    
    #path('registro',registro, name = 'registro')
]