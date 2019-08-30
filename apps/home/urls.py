from django.urls import path, re_path
from .views import registro, Home

urlpatterns = [
    path('', Home, name = 'index'),
    #path('registro',registro, name = 'registro')
]