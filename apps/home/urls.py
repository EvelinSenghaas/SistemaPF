from django.urls import path, re_path
from .views import registro
from .views import Home

urlpatterns = [
    path('', Home, name = 'index'),
    path('registracion/',registro, name = 'registracion')
]