from django.shortcuts import render, redirect
from directmessages.apps import Inbox
from directmessages.models import Message
from django.http import HttpResponseRedirect, HttpResponse
import json
from datetime import datetime, timedelta
    
from django.contrib.auth.models import User
from ..home.models import Alumno, FichaAlumno, Profesor, Semana, DisponibilidadProfesor
from ..rutina.models import Rutina, Actividad, Detalle, Nivel, Repeticion, EvaluacionNivel, Sesion, Revision, EsfuerzoActividad, RevisionSesion



def inbox(request, pk1, pk2):
    #pk1 emisor
    #pk2 receptor
    userEmisor = User.objects.get(id=pk1)
    userReceptor = User.objects.get(id=pk2)
    
    if (Alumno.objects.filter(user_id=userEmisor.id).exists()):
        #quiere decir que el alumno es emisor
        emisor = Alumno.objects.get(user_id=userEmisor.id)
    else:
        #quiere decir que el profesor es el emisor
        emisor = Profesor.objects.get(user_id=userEmisor.id)
        
    if (Alumno.objects.filter(user_id=userReceptor.id).exists()):
        #quiere decir que el alumno es receptor
        receptor = Alumno.objects.get(user_id=userReceptor.id)
    else:
        #quiere decir que el profesor es el receptor
        receptor = Profesor.objects.get(user_id=userReceptor.id)
    
    
    if request.method == 'GET':
        mensajesNoLeidos = Inbox.get_unread_messages(userEmisor)
        conversacion = Inbox.get_conversation(userEmisor, userReceptor, 30)
        ultimoMensaje = Inbox.get_conversation(userEmisor, userReceptor, 1, True)
        for ult in ultimoMensaje:
            ultimoMensaje = ult
        print(ultimoMensaje)
        return render (request, 'chat/inbox.html', {'emisor':emisor, 'receptor':receptor, 'mensajesNoLeidos':mensajesNoLeidos, 'ultimoMensaje':ultimoMensaje})


def inboxProfesor(request, pk):
    pass
    user = User.objects.get(id=pk)
    if not (Profesor.objects.filter(user_id=user.id).exists()):
        return redirect('/home')
    else:
        profesor = Profesor.objects.get(user_id=user.id)
        mensajes = []
        alumnos = Alumno.objects.filter(profesor_id=profesor.id)
        for alumno in alumnos:
            if (Message.objects.filter(sender=User.objects.get(id=alumno.user_id), recipient=user.id).exists()):
                mensajes.append(Message.objects.filter(sender=User.objects.get(id=alumno.user_id), recipient=user.id).latest('sent_at'))
        print(mensajes)              
        return render (request, 'chat/inbox_profesor.html', {'mensajes':mensajes})
        pass
    
def escribirMensaje(request):
    if request.method == 'POST':
        peticion = request.POST.copy()
        
        receptor = peticion.pop('receptor')
        receptor = receptor[0]
        receptor = User.objects.get(id=receptor)
        
        emisor = peticion.pop('emisor')
        emisor = emisor[0]
        emisor = User.objects.get(id=emisor)
        
        mensaje = peticion.pop('mensaje')
        
        Inbox.send_message(emisor, receptor, mensaje)
    else:
        return render (request, 'chat/escribirMensaje.html')
    return redirect('/chat/escribir_mensaje')


def verConversacion (request):
    print(request.GET['idReceptor'])
    print(request.GET['idEmisor'])
    userReceptor = User.objects.get(id=request.GET['idReceptor'])     
    userEmisor = User.objects.get(id=request.GET['idEmisor'])
    
    conversacionAux = Inbox.get_conversation(userEmisor, userReceptor, 50)
    conversacion = []
    dic = {}
    for conver in conversacionAux:
        ahora = conver.sent_at
        ahora = ahora - timedelta(hours=3)
        dic = {
        'content': conver.content,
        'sender': conver.sender.id,
        'recipient': conver.recipient.id,
        'sent_at': str(ahora.strftime('%d %b. %Y %H:%M')),
        'idMensaje': str(conver.id)
        }
        conversacion.append(dic)
    
    return HttpResponse(
                json.dumps(conversacion),
                content_type="application/json")
    
def enviarMensaje(request):

    
    userReceptor = User.objects.get(id=request.GET.get('idReceptor', None))     
    userEmisor = User.objects.get(id=request.GET.get('idEmisor', None))
    mensaje = str(request.GET.get('mensaje', None))
    
    if mensaje != '':
        mensaje = Inbox.send_message(userEmisor, userReceptor, mensaje)
        
        dic = {}
        
        dic['idReceptor'] = str(userReceptor.id)
        dic['idEmisor'] = str(userReceptor.id)
        dic['mensaje'] = str(mensaje)
    
    
    return HttpResponse(
                json.dumps(dic),
                content_type="application/json")
    

def obtenerUltimosMensajes(request):
    userReceptor = User.objects.get(id=request.GET.get('idReceptor', None))     
    userEmisor = User.objects.get(id=request.GET.get('idEmisor', None))
    
    mensajesNoLeidosAux = Inbox.get_unread_messages(userEmisor)
    mensajesNoLeidos = []
    dic = {}
    for msj in mensajesNoLeidosAux:
        ahora = msj.sent_at
        ahora = ahora - timedelta(hours=3)
        dic = {
        'content': msj.content,
        'sender': msj.sender.id,
        'recipient': msj.recipient.id,
        'sent_at': str(ahora.strftime('%d %b. %Y %H:%M')),
        'idMensaje': str(msj.id)
        }
        mensajesNoLeidos.append(dic)
    
    return HttpResponse(
                json.dumps(mensajesNoLeidos),
                content_type="application/json")
    
    
def vistoMensaje(request):
    msj = request.GET['mensaje']
    data = {}
    print
    mensaje = Message.objects.get(id=msj)
    print(type(mensaje))
    Inbox.read_message(mensaje.id)
    
    print(mensaje)
    return HttpResponse(
                json.dumps(data),
                content_type="application/json")
    
    
def ocultarMensajes(request):
    user = User.objects.get(id=request.GET['id'])
    data = {}
    
    if not(user.is_staff):
        if (Alumno.objects.filter(user_id=user.id).exists()):
            alumno = Alumno.objects.get(user_id=user.id)
            data['profesor_id'] = str(alumno.profesor_id.user_id)
            d = False
            data['ocultar'] = d
            p = False
            data['profesor'] = p
            mensajesNoLeidos = Inbox.get_unread_messages(alumno.user_id)
            c = len(mensajesNoLeidos)
            data['count']= c
        elif (Profesor.objects.filter(user_id=user.id).exists()):
            profesor = Profesor.objects.get(user_id=user.id)
            data['profesor_id'] = profesor.user_id
            d = False
            data['ocultar'] = d
            p = True
            data['profesor'] = p
            mensajesNoLeidos = Inbox.get_unread_messages(profesor.user_id)
            c = len(mensajesNoLeidos)
            data['count']= c
    else:
        p = None
        data['profesor_id'] = p
        d = True
        data['ocultar'] = d
        p = False
        data['profesor'] = p
        c = 0
        data['count']= c
        
    print(data['ocultar'])
    
    return HttpResponse(
                json.dumps(data),
                content_type="application/json")