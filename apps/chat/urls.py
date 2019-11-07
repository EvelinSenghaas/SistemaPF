from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from .views import escribirMensaje, inbox, verConversacion, enviarMensaje, obtenerUltimosMensajes, vistoMensaje


urlpatterns = [
    path('inbox/<int:pk1>/<int:pk2>', inbox, name='inbox'),
    path('escribir_mensaje/', escribirMensaje, name='escribir_mensaje'),
    path('ver_conversacion_ajax/', verConversacion, name='ver_conversacion_ajax'),
    path('enviar_mensaje_ajax/', enviarMensaje, name='enviar_mensaje_ajax'),
    path('obtener_ultimos_mensajes_ajax/', obtenerUltimosMensajes, name='obtener_ultimos_mensajes_ajax'),
    path('visto_mensaje_ajax/', vistoMensaje, name='visto_mensaje_ajax'),
    
]    