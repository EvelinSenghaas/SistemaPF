from django.shortcuts import render, redirect
from .models import Rutina, Actividad, Detalle, Nivel, Repeticion, EvaluacionNivel, Sesion, Revision
from ..home.models import Alumno, FichaAlumno, Profesor, Semana, DisponibilidadProfesor
from ..home.forms import AlumnoForm, FichaForm
from .forms import DetalleForm, ActividadForm, RutinaForm, NivelForm, RepeticionForm, EvaluacionNivelForm
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.mixins import PermissionRequiredMixin
from apps.home.models import Profesor
from django.contrib.auth.models import User
import operator
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.core import serializers
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


from django.utils import timezone
import time
import calendar
from datetime import datetime, date
from datetime import date


# Create your views here.
    
class Rutinas (PermissionRequiredMixin,ListView):
    permission_required = ('rutina.view_rutina', 'rutina.add_rutina')
    template_name = 'rutina/administrarRutinas.html'
    context_object_name = 'rutinas'
    queryset = Rutina.objects.all()
    

#Listados
class ListadoRutinas (PermissionRequiredMixin,ListView):
    permission_required = ('rutina.view_rutina')
    template_name = 'rutina/rutinas.html'
    context_object_name = 'rutinas'
    queryset = Rutina.objects.filter(estado=True)

class ListadoActividades (PermissionRequiredMixin,ListView):
    permission_required = ('rutina.add_actividad')
    template_name = 'rutina/actividades.html'
    context_object_name = 'actividades'
    queryset = Actividad.objects.filter(estado=True)
    
class ListadoDetalles (PermissionRequiredMixin,ListView):
    permission_required = ('rutina.add_detalle')
    template_name = 'rutina/administrarDetalles.html'
    context_object_name = 'detalles'
    queryset = Detalle.objects.filter(estado=True)
    
def traducirDia(dia):
    if dia == "Sunday":
        dia = "Domingo"
    if dia == "Monday":
        dia = "Lunes"    
    if dia == "Tuesday":
        dia = "Martes"
    if dia == "Wednesday":
        dia = "Miercoles"  
    if dia == "Thursday":
        dia = "Jueves"
    if dia == "Friday":
        dia = "Viernes"  
    if dia == "Saturday":
        dia = "Sabado"
    return dia


    
#Metodo para calcular el nivel a asignar al alumno
def calcularNivel(altura, circu, peso, actividad, sexo):
    print(type(altura))
    
    if sexo == 'M':
        contextura = (float(altura)/float(circu))
        if contextura > 10.4:
            nombreContextura = "pequeña"
        if 9.6 <= contextura <= 10.4:
            nombreContextura = "mediana"
        if contextura < 9.6:
            nombreContextura = "grande"
    else:
        contextura = (float(altura)/float(circu))
        if contextura > 11:
            nombreContextura = "pequeña"
        if 10.1 <= contextura <= 11:
            nombreContextura = "mediana"
        if contextura < 10.1:
            nombreContextura = "grande"

    altura = float(altura)/100
    imc = float(peso) / (altura*altura)
    if imc < 18.4:
        nombreImc = "delgado"
    if 18.4 <= imc <= 24.9:
        nombreImc = "normal"
    if imc > 24.9:
        nombreImc = "gordo"


    if actividad == "mucho":
        if (nombreImc == "delgado") or (nombreImc == "normal"):
            nivel = "avanzado"
        else:
            if (nombreContextura == "grande"):
                nivel = "intermedio"
            if (nombreContextura == "pequeña") or (nombreContextura == "mediana"):
                nivel = "principiante"
        return nivel
    if actividad == "poco":
        if (nombreImc == "delgado") or (nombreImc == "normal"):
            nivel = "intermedio"
        if (nombreImc == "gordo"):
            nivel = "principiante"
        return nivel
    if actividad == "nada":
        if (nombreImc == "delgado"):
            nivel = "intermedio"
        else:
            nivel = "principiante"
        return nivel
    


def calcularCantidadActividades(alumno, auxActividades, sesionesPorNivel, sesionesAlumno):
    pass
    """ 
        PRINCIPIANTE
                    x < 40
                            una por musculo (2)
                    40 <= x <= 65
                            incremenetamos una mas por musculo (4)
                    x > 65
                            incremenetamos una mas por musculo (6)
                            
                            
        INTERMEDIO
                    x < 25
                            una por musculo (2)
                    25 <= x < 50
                            incremenetamos una mas por musculo (4)
                    50 <= x < 75
                            incremenetamos una mas por musculo (6)
                    75 <= x
                            incremenetamos una mas por musculo (8)
                            
        AVANZADO
                    x < 20
                            una por musculo (2)
                    20 <= x < 40
                            incremenetamos una mas por musculo (4)
                    40 <= x 60
                            incremenetamos una mas por musculo (6)
                    60 <= x < 80
                            incremenetamos una mas por musculo (8)
                    80 <= x
                            incremenetamos una mas por musculo (10)
    """
    repeticiones = []
    porcentaje = (sesionesAlumno * 100) / sesionesPorNivel
    
    if alumno.nivel_id.nombre == "Principiante":
        if porcentaje < 40:
            trenSuperior = 1
            trenInferior = 1
            for acti in auxActividades:
                for det in acti.detalle_id.all():
                    if (det.categoria == "Tren Superior" and trenSuperior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenSuperior -=1
                        break
                    if (det.categoria == "Tren inferior" and trenInferior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenInferior -=1
                        break
        
        if 40 <= porcentaje <= 65:
            trenSuperior = 2
            trenInferior = 2
            for acti in auxActividades:
                for det in acti.detalle_id.all():
                    if (det.categoria == "Tren Superior" and trenSuperior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenSuperior -=1
                        break
                    if (det.categoria == "Tren inferior" and trenInferior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenInferior -=1
                        break
        
        if porcentaje > 65:
            trenSuperior = 3
            trenInferior = 3
            for acti in auxActividades:
                for det in acti.detalle_id.all():
                    if (det.categoria == "Tren Superior" and trenSuperior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenSuperior -=1
                        break
                    if (det.categoria == "Tren inferior" and trenInferior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenInferior -=1
                        break
        
    
    if alumno.nivel_id.nombre == "Intermedio":
        if porcentaje < 25:
            trenSuperior = 1
            trenInferior = 1
            for acti in auxActividades:
                for det in acti.detalle_id.all():
                    if (det.categoria == "Tren Superior" and trenSuperior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenSuperior -=1
                        break
                    if (det.categoria == "Tren inferior" and trenInferior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenInferior -=1
                        break
        
        if 25 <= porcentaje < 50:
            trenSuperior = 2
            trenInferior = 2
            for acti in auxActividades:
                for det in acti.detalle_id.all():
                    if (det.categoria == "Tren Superior" and trenSuperior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenSuperior -=1
                        break
                    if (det.categoria == "Tren inferior" and trenInferior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenInferior -=1
                        break
        
        if 50 <= porcentaje < 75:
            trenSuperior = 3
            trenInferior = 3
            for acti in auxActividades:
                for det in acti.detalle_id.all():
                    if (det.categoria == "Tren Superior" and trenSuperior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenSuperior -=1
                        break
                    if (det.categoria == "Tren inferior" and trenInferior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenInferior -=1
                        break
                    
        if 75 <= porcentaje:
            trenSuperior = 4
            trenInferior = 4
            for acti in auxActividades:
                for det in acti.detalle_id.all():
                    if (det.categoria == "Tren Superior" and trenSuperior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenSuperior -=1
                        break
                    if (det.categoria == "Tren inferior" and trenInferior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenInferior -=1
                        break
               
                    
    if alumno.nivel_id.nombre == "Avanzado":
        if porcentaje < 20:
            trenSuperior = 1
            trenInferior = 1
            for acti in auxActividades:
                for det in acti.detalle_id.all():
                    if (det.categoria == "Tren Superior" and trenSuperior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenSuperior -=1
                        break
                    if (det.categoria == "Tren inferior" and trenInferior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenInferior -=1
                        break   
        
        if 20 <= porcentaje < 40:
            trenSuperior = 2
            trenInferior = 2
            for acti in auxActividades:
                for det in acti.detalle_id.all():
                    if (det.categoria == "Tren Superior" and trenSuperior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenSuperior -=1
                        break
                    if (det.categoria == "Tren inferior" and trenInferior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenInferior -=1
                        break  
                    
        if 40 <= porcentaje < 60:
            trenSuperior = 3
            trenInferior = 3
            for acti in auxActividades:
                for det in acti.detalle_id.all():
                    if (det.categoria == "Tren Superior" and trenSuperior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenSuperior -=1
                        break
                    if (det.categoria == "Tren inferior" and trenInferior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenInferior -=1
                        break     
                    
        if 60 <= porcentaje < 80:
            trenSuperior = 4
            trenInferior = 4
            for acti in auxActividades:
                for det in acti.detalle_id.all():
                    if (det.categoria == "Tren Superior" and trenSuperior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenSuperior -=1
                        break
                    if (det.categoria == "Tren inferior" and trenInferior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenInferior -=1
                        break   
                    
        if 80 <= porcentaje:
            trenSuperior = 5
            trenInferior = 5
            for acti in auxActividades:
                for det in acti.detalle_id.all():
                    if (det.categoria == "Tren Superior" and trenSuperior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenSuperior -=1
                        break
                    if (det.categoria == "Tren inferior" and trenInferior != 0):
                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                        trenInferior -=1
                        break  
    
    return repeticiones
        

def actualizarFicha(request):
    if request.method == 'POST':
        print('ENTRO AL POST DE LA FUNCION ACTUALIZAR FICHA')
        peticion = request.POST.copy()
        print(peticion)
        #Obtenemos el usuario y el alumno
        us = peticion.pop('user')
        us = us[0]
        user = User.objects.get(id=us)
        alumno = Alumno.objects.get(user_id=user.id)
            
        clase = peticion.pop('clase')
        clase = clase[0]
        
        if clase == '1':
            print('ENTRA EN LA SELECCION DE HORARIO')
            disp = peticion.pop('disponibilidad')
            disp = disp[0]
            DisponibilidadProfesor.objects.filter(id=int(disp)).update(alumno_id=alumno, ocupado=True)
            return render(request, 'rutina/clases.html', {'alumno':alumno})
        
        if clase == '0':    
            print('ENTRA EN LA ACTUALIZACION DE DATOS')
            
            ficha = FichaAlumno.objects.get(alumno_id=alumno.id)
            
            altura = ficha.altura
            
            circu = peticion.pop('circu')
            circu = circu[0]
            
            peso = peticion.pop('peso')
            peso = peso[0]
            
            sexo = ficha.sexo
            
            print(altura)
            print(circu)
            print(peso)
            #Obtenemos cuanta actividad hace el alumno
            if len(alumno.semana_id.all()) <= 2:
                actividad = "poco"
            if len(alumno.semana_id.all()) >= 3:
                actividad = "mucho"
            if len(alumno.semana_id.all())  == 0:
                actividad = "nada"
                
            #Recalculamos el nivel
            nivel = calcularNivel(altura, circu, peso, actividad, sexo)
            nivel = nivel.capitalize()
            print(nivel)
            
            if nivel != str(alumno.nivel_id.nombre):
                Alumno.objects.filter(id=alumno.id).update(nivel_id=Nivel.objects.get(nombre=nivel))
                FichaAlumno.objects.filter(alumno_id=alumno.id).update(peso = float(peso), circunferenciaMuneca = float(circu))
                #ACA DEBEMOS CAMBIAR A TRUE EL ATRIBUTO CLASE DE REVISION
                mensaje3= "Subiste de nivel, ahora solo falta que tu profesor te evalúe. Para ello, debes elegir qué día queres tener una clase presencial"
                disponibilidad = DisponibilidadProfesor.objects.filter(profesor_id=alumno.profesor_id, ocupado=False)
                print(disponibilidad)
            else:
                mensaje3= None   
                   
            return render(request, 'rutina/actualizarFicha.html', {'alumno':alumno, 'mensaje3': mensaje3, 'disponibilidad': disponibilidad}) 
    
    #return render (request, 'rutina/clases.html', {'alumno':alumno, "mensaje3":mensaje3})
    else:
        print('get de la funcion correcta')
        return render (request, 'rutina/actualizarFicha.html')
    
    
        
    """
    print('Llego al limite de sesiones, se debe recalcular el nivel')
                    #Obtenemos los datos necesarios para recalcular el nivel
                    ficha = FichaAlumno.objects.get(alumno_id = alumno.id)
                    altura = ficha.altura
                    circu = ficha.circunferenciaMuneca
                    peso = ficha.peso
                    sexo = ficha.sexo
                    
                    
                    x <= 2
                        poco
                    x >= 3
                        mucho
                    x = 0
                        nada
                    
                    #Obtenemos cuanta actividad hace el alumno
                    if len(alumno.semana_id) <= 2:
                        actividad = "poco"
                    if len(alumno.semana_id) >= 3:
                        actividad = "mucho"
                    if len(alumno.semana_id)  == 0:
                        actividad = "nada"
                    
                    
                    #Recalculamos el nivel
                    nivel = calcularNivel(altura, circu, peso, actividad, sexo)
                    nivel = nivel.capitalize()
                    print(nivel)
                    if nivel != str(alumno.nivel_id.nombre):
                        Alumno.objects.filter(id=alumno.id).update(nivel_id=Nivel.objects.get(nombre=nivel))
                        #ACA DEBEMOS CAMBIAR A TRUE EL ATRIBUTO CLASE DE REVISION
                        mensaje2= "Subiste de nivel, ahora solo falta que tu profesor te evalúe"
                    else:
                        mensaje2= None
                    
                    
                else:
                    print('Todavia no llego al limite de sesiones')
    """    
        



def verClase(request, pk):
    user = User.objects.get(id=pk)
    
    #si entra un alumno
    if (Alumno.objects.filter(user_id=user.id).exists()):
        alumno = Alumno.objects.get(user_id=user.id)
        profesor = alumno.profesor_id
        rutina = alumno.rutina_id
        print('rutina: ' +rutina.nombre)
        
        #si entrena con un profesor
        if not alumno.entrenamiento_sistema:
            if request.method == 'GET':
                disponibilidad = DisponibilidadProfesor.objects.filter(alumno_id=alumno.id)
                
                now = datetime.now()
                dia = now.strftime("%A")
                dia = traducirDia(dia)
                
                
                diasAlumno=[]
                for disp in disponibilidad:
                    diasAlumno.append(Semana.objects.get(dia=disp.semana_id))
                
                diasAlumno = sorted(diasAlumno, key=lambda diasAlumno: diasAlumno.numero)
                print(diasAlumno)
                
                clase=None
                i=0
                while i< len(diasAlumno):    
                    if dia == diasAlumno[i].dia:
                        mensaje = None
                        hora_inicio = DisponibilidadProfesor.objects.get(alumno_id=alumno.id, semana_id=diasAlumno[i]).horario_inicio
                        hora_final = DisponibilidadProfesor.objects.get(alumno_id=alumno.id, semana_id=diasAlumno[i]).horario_final
                        
                        if now.time() < hora_inicio:
                            clase = "Tienes una clase con " + str(alumno.profesor_id)  + " hoy desde las " + hora_inicio.strftime("%H:%M") + " hasta las " + hora_final.strftime("%H:%M") +"hs."
                        
                        if  hora_inicio <= now.time() <= hora_final:
                            clase = "La clase con " + str(alumno.profesor_id)  + " esta en curso. "
                        
                        if now.time() > hora_final:
                            clase = None
                            mensaje = "Tu clase con " + str(alumno.profesor_id) + " ya ha terminado."
                            break
                        break
                         
                    else:
                        mensaje = "Hoy no es día de entrenamiento, debes esperar a tu próxima clase"
                    
                    i+=1
                        
                return render (request, 'rutina/clases.html', {'alumno':alumno, "mensaje":mensaje, 'disponibilidad':disponibilidad, 'clase':clase, 'profesor':profesor})
        
        #Si entrena por el sistema    
        else:
            if request.method == 'GET':
                alumno = Alumno.objects.get(user_id=pk)
                #Obtengo el dia y fecha de hoy
                now = datetime.now()
                today = date.today()
                dia = now.strftime("%A")
                dia = traducirDia(dia)
                fechaActual = today.strftime("%d/%m/%Y")
                print(fechaActual)
                print(dia)
                
                diasAlumno=[]
                for d in alumno.semana_id.all():
                    diasAlumno.append(Semana.objects.get(id=d.id))
                
                diasAlumno = sorted(diasAlumno, key=lambda diasAlumno: diasAlumno.numero)
                print(diasAlumno)
                
                i=0
                while i < len(diasAlumno):
                    print(str(dia) +' ' + str(diasAlumno[i].dia))
                    if str(dia) == str(diasAlumno[i].dia):
                        #Si entra aca es porque hoy SI es el dia de entrenamiento
                        mensaje = None
                        
                        if (Sesion.objects.filter(alumno_id = alumno).exists()):
                            #Ya tiene sesiones, por lo tanto, se debe comparar actividades anteriores y la cantidad de sesiones faltantes para recalcular el nivel
                            
                            #Obtengo la ultima sesion del alumno
                            ultimaSesion = Sesion.objects.filter(alumno_id=alumno.id).latest()
                            if ultimaSesion.claseRevision == False:
                                print(ultimaSesion)
                                if today != ultimaSesion.fechaSesion:
                                    #No hizo la sesion de hoy
                                    """Procedimientos
                                            * debo obtener las actividades y sacar aquellas que ya hizo en la ultima sesion SI ES QUE HAY OTRAS   
                                            * """
                                    print(today)
                                    actividades = rutina.actividad_id.all()
                                    actividadesRealizadas = ultimaSesion.actividad_id.all()
                                    print('Actividades realizadas en la ultima sesion\n'+str(actividadesRealizadas))
                                    print('Actividades de la rutina\n'+str(actividades))
                                    
                                    #Sacamos las actividades de la clase anterior
                                    auxActividades = []
                                    auxActividades = list(actividades)
                                    list(actividadesRealizadas)
                                    for i in actividadesRealizadas:
                                        auxActividades.remove(i)                   
                                    print('Actividades supuestamente filtradas\n'+str(auxActividades))
                                    
                                    
                                    """ Debemos decidir cuantas actividades darle dependiendo del porcentaje de sesiones que lleva realizando
                                        Hacemos
                                                Hasta el 40%  solo uno por musculo
                                                Entre 40%  y 60%  incrementamos uno por musculo
                                                Entre 60%  y 80%  incrementamos uno por musculo
                                                Mas de 80%  incrementamos uno por musculo
                                    """
                                    
                                    #Obtenemos la cantidad de sesiones que debe hacer segun el nivel y las que lleva
                                    sesionesPorNivel = EvaluacionNivel.objects.get(nivel_id = alumno.nivel_id).cantSesiones
                                    sesionesAlumno = ultimaSesion.cantSesiones
                                    
                                    #Obtenemos las repeticiones que debe hacer segun su nivel y el porcentaje de avance en el nivel
                                    repeticiones = calcularCantidadActividades(alumno, auxActividades, sesionesPorNivel, sesionesAlumno)         
                                    
                                    mensaje = None
                                    return render (request, 'rutina/clases.html', {'alumno':alumno, "mensaje":mensaje, 'repeticiones':repeticiones})
                                    
                                else:
                                    #Ya hizo la sesion de hoy
                                    mensaje = "Gracias por entrenarte con nosotros, tu sesión ha terminado. Vuelve el "
                                    return render (request, 'rutina/clases.html', {'alumno':alumno, "mensaje":mensaje})
                            else:
                                if str(dia) == str(DisponibilidadProfesor.objects.get(alumno_id=alumno.id).semana_id.dia):
                                    #La clase de hoy es una de revision
                                    print('entra donde quieroo')
                                    mensaje = "Hoy te toca una clase dictada por " + str(alumno.profesor_id) + " a las HORA"
                                    return render (request, 'rutina/clases.html', {'alumno':alumno, "mensaje":mensaje})
                                
                                else:
                                    mensaje = "Hoy no es tu día de entrenamiento, vuelve el "
                                    return render (request, 'rutina/clases.html', {'alumno':alumno, "mensaje":mensaje}) 
                            
                            
                                    
                            
                        else:
                            #Si es la primera sesion del alumno
                            actividades = rutina.actividad_id.all()
                            print('actividades: ' +str(actividades.all()))
                            actividadesARealizar = []
                            repeticiones = []
                            trenSuperior = False
                            trenInferior = False
                            for acti in actividades.all():
                                for det in acti.detalle_id.all():
                                    if (det.categoria == "Tren Superior" and trenSuperior == False):
                                        print('Entra en tren superior')
                                        actividadesARealizar.append(acti)
                                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                                        trenSuperior = True
                                        break
                                    if (det.categoria == "Tren inferior" and trenInferior == False):
                                        print('Entra en tren inferior')
                                        actividadesARealizar.append(acti)
                                        repeticiones.append(Repeticion.objects.get(actividad_id=acti.id, nivel_id=alumno.nivel_id))
                                        print(repeticiones)
                                        trenInferior = True
                                        break

                        return render (request, 'rutina/clases.html', {'alumno':alumno, "mensaje":mensaje, 'actividadesARealizar':actividadesARealizar, 'repeticiones':repeticiones}) 
                    
                    
                    print(len(diasAlumno))
                     
                    if str(dia) != str(diasAlumno[i].dia) and i==len(diasAlumno)-1:
                        #Si entra aca es porque hoy NO es el dia de entrenamiento
                        mensaje = "Hoy no es tu día de entrenamiento, vuelve el "
                        return render (request, 'rutina/clases.html', {'alumno':alumno, "mensaje":mensaje})  
                        break
                    
                    i+=1
                        
                        
                return render (request, 'rutina/clases.html', {'alumno':alumno, "mensaje":mensaje})   
            else:
                today = date.today()
                print('entro al post')
                peticion = request.POST.copy()
                print(peticion)          
                
                #Obtenemos los datos requeridos de la sesion (SE DEBE CONTROLAR CON TRY EXCEP DESPUES)
                repe = peticion.pop('repeticiones')
                repeticiones = []
                for r in repe:
                    repeticiones.append(Repeticion.objects.get(id=r))
                
                
                esfuerzo = peticion.pop('esfuerzo')
                esfuerzo = esfuerzo[0]
                int(esfuerzo)
                descripcion = peticion.pop('descripcion')
                descripcion = descripcion[0]
                print('            ')
                print(esfuerzo)
                print(repeticiones)
                print(descripcion)
                print('             ')
                actividades = []
                
                #cargo las actividades que el alumno realizo                
                for r in repeticiones:
                    actividades.append(r.actividad_id)
                
                sesionesAlumno = Sesion.objects.filter(alumno_id = alumno)
                if len(sesionesAlumno) != 0:
                    #Obtenemos la ultima sesion del alumno
                    ultimaSesion = Sesion.objects.filter(alumno_id=alumno.id).latest()
                
                #creamos la nueva sesion
                sesion = Sesion.objects.create(alumno_id=alumno, rutina_id=rutina, profesor_id=profesor)
                for a in actividades:
                    print(type(a))
                    sesion.actividad_id.add(a)
                sesion.fechaSesion = today
                sesion.esfuerzoSesion = esfuerzo
                print('le cargo el esfuerzo')
                sesion.descripcion = descripcion
                print('le cargo la descripcion')
                

                #Si el chico no tiene sesion (debo asignarle 1 porque es la primer sesion)
                sesionesAlumno = Sesion.objects.filter(alumno_id = alumno)
                print(len(sesionesAlumno))
                if(len(sesionesAlumno) == 1):
                    print('le puso uno en cantSesiones y sesionesRealizadas')
                    sesion.cantSesiones = int(1)
                    sesion.sesionesRealizadas = int(1)
                else:
                    print('entro al else, osea ya tiene sesion')
                    #tengo que obtener la sesion y actualizar las cosas
                    print(ultimaSesion)
                    
                    #Obtenemos las sesiones parciales y totales
                    cantSesiones = ultimaSesion.cantSesiones + 1
                    sesionesRealizadas = ultimaSesion.sesionesRealizadas + 1
                    
                    sesion.cantSesiones = cantSesiones
                    sesion.sesionesRealizadas = sesionesRealizadas
                
                sesion.save()
                
                
                #Se vuelve a obtener la ultima sesion (la que acaba de guardarse) del alumno para ver si completo todas las sesiones
                sesionActual = Sesion.objects.filter(alumno_id=alumno.id).latest()
                
                try:
                    check = peticion.pop('check')
                    check = check[0]
                    print(check)
                    if check != None:
                        print('selecciono')
                        revision = Revision.objects.create(profesor_id=profesor, sesion_id=sesion)
                        revision.save()
                except:
                    pass
                
                    
                #Se controla si con la sesion que acaba de realizar llego al 100% de las sesiones
                if sesionActual.cantSesiones == EvaluacionNivel.objects.get(nivel_id=alumno.nivel_id).cantSesiones:
                    print('entra donde quiero')
                    #Redireccionamos a la pagina de actualizacion de datos
                    #return redirect('/rutinas/actualizar_ficha/')
                    ficha = FichaAlumno.objects.get(alumno_id=alumno.id)
                    Sesion.objects.filter(id=sesionActual.id).update(claseRevision=True)
                    
                    mensaje = "Debes actualizar los datos de tu ficha de entrenamiento para que podamos evaluar tu nivel nuevamente"
                    
                    #return render_to_response ('rutina/actualizarFicha.html', context = {'alumno':alumno,'ficha':ficha, "mensaje":mensaje})
                    return redirect ('/rutinas/actualizar_ficha/')
                
                else:     
                    print('sigue donde no debe seguir')
                    mensaje = "Gracias por entrenarte con nosotros, tu sesión ha terminado. Vuelve el "
                    return render (request, 'rutina/clases.html', {'alumno':alumno, "mensaje":mensaje}) 
                
                print('aca no deberia estar')  
                    
                    
                    
                        
    
    
    #si entra un profesor    
    if (Profesor.objects.filter(user_id=pk).exists()):
        profesor = Profesor.objects.get(user_id=user.id)
        if request.method == 'GET':
            
            #Obtenemos el dia actual
            now = datetime.now()
            dia = now.strftime("%A")
            dia = traducirDia(dia)
            dia = Semana.objects.get(dia=dia)
            
            if (DisponibilidadProfesor.objects.filter(profesor_id=profesor.id, semana_id=dia, ocupado=True).exists()):
                alumnos = DisponibilidadProfesor.objects.filter(profesor_id=profesor.id, semana_id=dia, ocupado=True)
                mensaje = None
            else:
                mensaje = "Por hoy no tenes más alumnos que atender."
                alumnos = 'vacio'
            
            alumnosPendientes = [] 
            if alumnos != 'vacio':                   
                for alumno in alumnos:
                    if now.time() < alumno.horario_inicio or alumno.horario_inicio <= now.time() <= alumno.horario_final:
                        alumnosPendientes.append(alumno)
                        mensaje = None
                    else:
                        mensaje = "Por hoy no tenes más alumnos que atender."
                    
        return render (request, 'rutina/clases.html', {'alumnos':alumnos, 'profesor':profesor, 'profesor':profesor, 'alumnosPendientes':alumnosPendientes, 'mensaje':mensaje})
        
                
    

def perfil(request, pk):
    if (Alumno.objects.filter(user_id=pk).exists()):
        if Alumno.objects.get(user_id = pk).entrenamiento_sistema:
            print('entrena por sistema')
            alumno = Alumno.objects.get(user_id=pk)
            print(alumno)
            edad = alumno.edad(alumno.fecha_nac)
            ficha = FichaAlumno.objects.get(alumno_id=alumno.id)
            mensaje = None
            disponibilidad = alumno.semana_id.all()
 
            try:
                sesiones = Sesion.objects.filter(alumno_id=alumno.id).order_by('-id')
                ultimaSesion = Sesion.objects.filter(alumno_id=alumno.id).latest()
                for sesion in sesiones:
                    sesion.cantSesiones = (sesion.sesionesRealizadas * 100) / EvaluacionNivel.objects.get(nivel_id=alumno.nivel_id).cantSesiones
            except:
                sesiones = None
                


            
            
            

        else:
            alumno = Alumno.objects.get(user_id=pk)
            edad = alumno.edad(alumno.fecha_nac)
            ficha = FichaAlumno.objects.get(alumno_id=alumno.id)
            mensaje = None
            disponibilidad = DisponibilidadProfesor.objects.filter(alumno_id = alumno.id)
            sesiones = None
            
    else:
        mensaje = "El alumno no existe"
        return redirect('/home/')
    
    return render (request, 'home/verPerfil.html', { 'alumno': alumno, 'mensaje':mensaje, 'ficha':ficha, 'edad':edad, 'disponibilidad':disponibilidad, 'sesiones':sesiones})
    
    
def verRutina(request, pk):
    rutina = Rutina.objects.get(id = pk)
    actividades = []
    act = Rutina.objects.values_list('actividad_id').filter(id=pk)
    for a in act:
        i=0
        actividades += Actividad.objects.filter(id=a[i], estado=True)
        i+=1
    return render (request, 'rutina/verRutina.html', { 'rutina': rutina, 'actividades':actividades})


def verRevisiones(request, pk):
    user = User.objects.get(id=pk)
    profesor = Profesor.objects.get(user_id=user.id)
    
    if request.method == 'GET':
        revisiones = Revision.objects.filter(profesor_id=profesor.id)
        print(revisiones[0].sesion_id.alumno_id.nombre)
        return render (request, 'rutina/verRevisiones.html', { 'revisiones': revisiones})


def verActividad(request, pk):
    actividad = Actividad.objects.get(id = pk)
    detalles = []
    det = Actividad.objects.values_list('detalle_id').filter(id=pk)
    print(det)
    repe =  Repeticion.objects.values_list('nivel_id','repeticionesMinimas').filter(actividad_id = pk)
    repeticiones ={}
    
    for r in repe:
        nivel = Nivel.objects.get(id=r[0])
        repeticiones.setdefault(nivel.nombre,r[1])  
          
    for a in det:
        i=0
        detalles += Detalle.objects.filter(id=a[i])
        i+=1
    return render (request, 'rutina/verActividad.html', { 'actividad': actividad, 'detalles':detalles,'repeticiones':repeticiones})
       

#Agregar    
class AgregarDetalle(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'rutina.add_detalle'
    model = Detalle
    form_class = DetalleForm
    template_name = 'rutina/agregarDetalle.html'
    success_message = 'Detalle agregado con éxito.'
    succes_name = reverse_lazy('/rutinas/administrar_detalles/')
    
class AgregarActividad(PermissionRequiredMixin, CreateView):
    permission_required = ('rutina.add_actividad' or 'ruitna.change_actividad')
    model = Actividad
    nivel = Nivel.objects.all()
    template_name = 'rutina/agregarActividad.html'
    form_class = ActividadForm
    second_form_class = RepeticionForm
    succes_name = reverse_lazy('/rutinas/actividades/')
    
    def get_context_data(self, **kwargs):
        context = super(AgregarActividad, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(self.request.GET)
        if 'form2' not in context:
            context['form2'] = self.second_form_class(self.request.GET)
        return context
    
    def post (self, request, *args, **kwargs):
        self.object = self.get_obgect
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)
        if form.is_valid() and form2.is_valid():
            repeticion = form2.save(commit = False)
            repeticion.actividad_id = form.save()
            repeticion.save()
            return HttpResponseRedirect(self.get_success_url)()
        else:
            return self.render_to_response(self.get_context_data(form=form, form2=form2))    

def listadoEvaluacionNivel (request,pk):
    user = User.objects.get(id=pk)
    if (Profesor.objects.filter(user_id=user.id).exists()):
        profesor = Profesor.objects.get(user_id=user.id)
    else: 
        return redirect ('home')
    
    if request.method == 'GET':
        evaluacionNivel = EvaluacionNivel.objects.filter(profesor_id=profesor.id)
        return render(request, 'rutina/administrarEvaluacionNivel.html', {'evaluacionNivel':evaluacionNivel})
    else:
        return redirect ('/rutinas/administrar_evaluacion_nivel/')
    
    
def agregarEvaluacionNivel(request, pk):
    user = User.objects.get(id=pk)
    if (Profesor.objects.filter(user_id=user.id).exists()):
        profesor = Profesor.objects.get(user_id=user.id)
    else: 
        return redirect ('home')
    
    if request.method == 'POST':
        form = EvaluacionNivelForm(request.POST)
        peticion = request.POST.copy()
        nivel = peticion.pop('nivel_id')
        nivel = nivel[0]
        
        if (EvaluacionNivel.objects.filter(nivel_id=nivel, profesor_id = profesor).exists()):
            error = 'No puede ingresar una evaluación de nivel para mas de un nivel'
            return render (request, 'rutina/agregarEvaluacionNivel.html', {'profesor':profesor, 'form':form, 'error':error})
        else:
            if form.is_valid():
                evaluacionNivel = form.save(commit=False)
                evaluacionNivel.profesor_id = profesor
                evaluacionNivel.save()
                messages.success(request, 'Evaluación de nivel agregada con éxito.')
            else:
                error = form.errors
                messages.error(request, 'No se pudo cargar, por favor verifique los datos ingresados')
    else:
        form = EvaluacionNivelForm()
        return render (request, 'rutina/agregarEvaluacionNivel.html', {'profesor':profesor, 'form':form})
    return redirect('/rutinas/administrar_evaluacion_nivel/2')
        

def editarEvaluacionNivel(request, pk):
    if (EvaluacionNivel.objects.filter(id=pk).exists()):
        form = EvaluacionNivel.objects.get(id=pk)
        profesor = form.profesor_id
        nivel_anterior = form.nivel_id
    else: 
        return redirect ('home') 
    
    if request.method == 'GET':
        form = EvaluacionNivelForm(instance=form)
        return render (request, 'rutina/agregarEvaluacionNivel.html', {'profesor':profesor, 'form':form})
    else:
        print('entro al post')
        form = EvaluacionNivelForm(request.POST, instance = form)
        peticion = request.POST.copy()
        nivel = peticion.pop('nivel_id')
        nivel = nivel[0]
        
        if (EvaluacionNivel.objects.filter(nivel_id=nivel, profesor_id = profesor).exists()):
            print('entro al primer if')
            if (EvaluacionNivel.objects.get(nivel_id=nivel, profesor_id = profesor).nivel_id != nivel_anterior):
                print('entro al segundo if')
                error = 'No puede ingresar una evaluación de nivel para mas de un nivel'
                return render (request, 'rutina/agregarEvaluacionNivel.html', {'profesor':profesor, 'form':form, 'error':error})
            else:
                if form.is_valid():
                    evaluacionNivel = form.save(commit=False)
                    evaluacionNivel.save()
                    messages.success = (request,'La evaluacion de nivel se cargó con éxito.')
                else:
                    error = form.errors
                    return render (request, 'rutina/agregarEvaluacionNivel.html', {'profesor':profesor, 'form':form, 'error':error})
        
    return redirect('/rutinas/administrar_evaluacion_nivel/2')
            
            
def agregarActividad(request):
    nivel = Nivel.objects.all() 
    error = None
    if request.method == 'POST':
        form = ActividadForm(request.POST, request.FILES)
        form2 = RepeticionForm(request.POST)
        
        peticion = request.POST.copy()
        peticion2 = request.FILES.copy()
        print(peticion2)
        print(peticion)
        
        
        nivel_id = peticion.pop('nivel_id')
        
        
        try:
            detalles = peticion.pop('detalle_id')
        except:         
            error = "\n Debe seleccionar los detalles"
            return render(request, 'rutina/agregarActividad.html',{'form':form, 'form2':form2,'nivel':nivel,'error':error})
        
        
        
        rep_min = peticion.pop('repeticionesMinimas')
        
        print(rep_min)
        
        unico = []

        
        for x in nivel_id:
            if x not in unico:
                unico.append(x)
                   
        if len(unico) < 3:
            error = form.errors
            error2 = "No puede seleccionar dos niveles iguales."
            return render(request, 'rutina/agregarActividad.html',{'form':form, 'form2':form2,'nivel':nivel,'error':error, 'error2':error2})
        
        if form.is_valid() and form2.is_valid():
                       
            print('sigue')
            
            
            actividad = form.save()
            actividad.gif = request.FILES.get('archivo')
            actividad.detalle_id.set(detalles)
            actividad.save()
            repeticion = form2.save(commit=False)
            acti = Actividad.objects.get(id=actividad.id)  
            i=0
            while i < len(nivel_id):
                r = Repeticion.objects.create(actividad_id = actividad, nivel_id = Nivel.objects.get(id = nivel_id[i]), repeticionesMinimas = rep_min[i])
                r.save()
                i+=1
            messages.success(request, 'Actividad agregada con éxito.')
        else:
            error = form.errors
            return render(request, 'rutina/agregarActividad.html',{'form':form, 'form2':form2,'nivel':nivel,'error':error})     
    else:
        form = ActividadForm()
        form2 = RepeticionForm()
        return render(request, 'rutina/agregarActividad.html',{'form':form, 'form2':form2,'nivel':nivel,'error':error})
    return redirect('/rutinas/actividades/')  


def editarActividad(request, pk):
    actividad = Actividad.objects.get(id = pk)
    repeticiones = Repeticion.objects.filter(actividad_id=pk)
    nivel = Nivel.objects.all() 
        
    if request.method == 'GET':
        form = ActividadForm(instance = actividad)
        form2 = RepeticionForm()
    else:
        form = ActividadForm(request.POST, instance = actividad)
        form2 = RepeticionForm(request.POST)
        
        peticion = request.POST.copy()
        
        try:
            detalles = peticion.pop('detalle_id')
        except:         
            error = "\n Debe seleccionar los detalles"
            return render(request, 'rutina/agregarActividad.html',{'form':form, 'form2':form2,'nivel':nivel,'error':error})
        
        
        nivel_id = peticion.pop('nivel_id')
        rep_min = peticion.pop('repeticionesMinimas')
        
        print(nivel_id)
        
        unico = []

        
        for x in nivel_id:
            if x not in unico:
                unico.append(x)
                   
        if len(unico) < 3:
            error = form.errors
            error2 = "No puede seleccionar dos niveles iguales."
            return render(request, 'rutina/agregarActividad.html',{'form':form, 'form2':form2,'nivel':nivel,'error':error, 'error2':error2})
        
        
        if form.is_valid() and form2.is_valid():
            actividad = form.save(commit = False)
            actividad.gif = request.FILES.get('archivo')
            actividad.detalle_id.set(detalles)
            actividad.save()
            form2.actividad_id = form
            form2.save(commit=False)
            i=0
            while i < len(nivel_id):
                Repeticion.objects.filter(actividad_id = actividad.id, nivel_id = nivel_id[i]).update(nivel_id = Nivel.objects.get(id = nivel_id[i]))
                Repeticion.objects.filter(actividad_id = actividad.id, nivel_id = nivel_id[i]).update(repeticionesMinimas = rep_min[i])
                i+=1
            messages.success(request, 'La actividad se modificó con éxito.')
        else:
            error = form.errors
            return render(request, 'rutina/agregarActividad.html',{'form':form, 'form2':form2,'nivel':nivel,'error':error}) 
            
        return redirect('/rutinas/actividades/') 
    return render(request, 'rutina/agregarActividad.html',{'form':form, 'form2':form2,'nivel':nivel})
            

#ESTO NO SE USA    
class AgregarRutina(PermissionRequiredMixin, CreateView):
    permission_required = 'rutina.add_rutina'
    model = Rutina
    form_class = RutinaForm
    template_name = 'rutina/agregarRutina.html'
    succes_name = reverse_lazy('/rutinas/administrar_rutinas/')
    
    def post(self,request, pk, *args, **kwargs):
        user = User.objects.get(id = pk)
        profesor = Profesor.objects.get(id=user.id)
        model.profesor_id=profesor.id
        model.save()
        return redirect('/rutinas')
    
def agregarRutina(request, pk):
    user = User.objects.get(id = pk)
    profesor = Profesor.objects.get(user_id=user.id)
    if request.method == 'POST':
        rutinaForm = RutinaForm(request.POST)
        peticion = request.POST.copy()
        try:
            actividades = peticion.pop('actividad_id')
        except:
            error = rutinaForm.errors
            error = error + "\n Debe seleccionar las actividades"
            return render(request, 'rutina/agregarRutina.html',{'rutinaForm':rutinaForm, 'error':error})
        
        print(request.POST)
        if rutinaForm.is_valid():
            rutina = rutinaForm.save(commit=False)
            rutina.profesor_id=profesor
            rutina.save()
            for act in actividades:
                rutina.actividad_id.add(act)
            rutina.save()
            messages.success(request, "La rutina se agregó correctamente.")
            return redirect ('/rutinas/administrar_rutinas/')
        else:
            print('entra al else')
            error = rutinaForm.errors
            return render(request, 'rutina/agregarRutina.html',{'rutinaForm':rutinaForm, 'error':error})
    else:
        rutinaForm = RutinaForm()
        return render(request, 'rutina/agregarRutina.html',{'rutinaForm':rutinaForm})
    
    return redirect ('/rutinas/administrar_rutinas/')
 
#Editar    
class EditarRutina(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'rutina.change_rutina'
    model = Rutina
    template_name = 'rutina/agregarRutina.html'
    form_class = RutinaForm
    success_message = 'La rutina se modificó correctamente.'
    succes_url = reverse_lazy('/rutinas/administrar_rutinas')
    

class EditarActividad(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'rutina.change_actividad'
    model = Actividad
    template_name = 'rutina/agregarActividad.html'
    form_class = ActividadForm
    success_message = 'La actividad se modificó con éxito.'
    succes_url = reverse_lazy('/rutinas/actividades/')
  
    
class EditarDetalle(PermissionRequiredMixin,SuccessMessageMixin, UpdateView):
    permission_required = 'rutina.change_detalle'
    model = Detalle
    template_name = 'rutina/agregarDetalle.html'
    form_class = DetalleForm
    success_message = 'El detalle se modificó con éxito.'
    succes_url = reverse_lazy('/rutinas/administrar_detalles')
    
#Eliminar
class EliminarRutina(DeleteView):
    model = Rutina
    def post(self,request, pk, *args, **kwargs):
        object = Rutina.objects.get(id = pk)
        if (Alumno.objects.filter(rutina_id=object.id).exists()):
            mensaje = "Usted no puede ocultar la rutina " + object.nombre + " debido a que la misma cuenta con alumnos inscriptos"
            return render(request, 'rutina/errorEliminacion.html',{'object':object, 'mensaje':mensaje})
        else:
            object.estado = not(object.estado)
            object.save()
        return redirect('/rutinas/administrar_rutinas')
    
def eliminarRutina(request, pk):
    rutina = Rutina.objects.get(id = pk)
    if (Alumno.objects.filter(rutina_id=rutina.id).exists()):
            messages.error(request, "Usted no puede ocultar la rutina " + rutina.nombre + " debido a que la misma cuenta con alumnos inscriptos")
    else:
        messages.success(request, "El estado de la rutina se cambió correctamente.")
        rutina.estado = not(rutina.estado)
        rutina.save()
        return redirect('/rutinas/administrar_rutinas')
    

def eliminarActividad(request, pk):
    actividad = Actividad.objects.get(id=pk)
    if (Rutina.objects.filter(actividad_id = actividad.id).exists()):
        print(Rutina.objects.filter(actividad_id = actividad))
        messages.error(request, 'La actividad no puede eliminarse debido a que forma parte de una rutina.')
    else:
        Actividad.objects.get(id = actividad.id).delete()
        messages.success(request, 'Actividad eliminada con éxito.')
        
    return redirect('/rutinas/actividades')
    
    
def eliminarDetalle(request, pk):
    detalle = Detalle.objects.get(id=pk)
    if (Actividad.objects.filter(detalle_id=detalle.id).exists()):
            messages.error(request, 'El detalle no puede eliminarse porque ya forma parte de una actividad')
    else:
        Detalle.objects.get(id = detalle.id).delete()
        messages.success(request, 'Detalle eliminado con éxito.')
        
    return redirect('/rutinas/administrar_detalles')
 

#No se usa
def BusquedaDisponibilidad(TemplateView):
    
    def get(self, request, *args, **kwargs):
        id_dia = request.GET['dia']
        disponibilidad = DisponibilidadProfesor.objects.filter(semana_id=id_dia)
        data = serializers.serialize('json',disponibilidad,
                                     fields=('id', 'horario_inicio','horario_final', 'semana_id'))
        return HttpResponse(data, content_type='application/json')
    
        
def inscribirseRutina(request, pk1, pk2):
    #Identificamos al user que se quiere inscribir (pk es de usuario)
    user = User.objects.get(id = pk1)
    #Identificamos la rutina a la que se quiere inscribir
    rutina = Rutina.objects.get(id = pk2) 
    
    disponibilidad = DisponibilidadProfesor.objects.filter(profesor_id=rutina.profesor_id, ocupado=False, alumno_id = None)
    dias = Semana.objects.all()
       
    if (user.is_staff):
        mensaje = "Usted pertenece al staff, por lo que no puede inscribirse a una rutina"
        return render (request, 'rutina/errorInscribirseRutina.html', { 'rutina': rutina, 'mensaje':mensaje})
        #Usted no puede inscribirse a la rutina     porque es un administrador
    else:
        if (Profesor.objects.filter(user_id=user.id).exists()):
            profesor = Profesor.objects.get(user_id = user.id)
            mensaje = "Usted es un profesor, por lo que no puede inscribirse a una rutina"
            return render (request, 'rutina/errorInscribirseRutina.html', { 'rutina': rutina, 'profesor':profesor, 'mensaje':mensaje})
            #Usted no se puede inscribir a la rutina     porque es un profesor
        elif (Alumno.objects.filter(user_id=user.id).exists()):
            alum = Alumno.objects.get(user_id=user.id)
            if (alum.rutina_id.id == Rutina.objects.get(id = alum.rutina_id.id).id):
                mensaje = "Usted esta inscipto a la rutina " + alum.rutina_id.nombre + ", por lo que primero debe darse de baja en la misma."
                return render (request, 'rutina/errorInscribirseRutina.html', { 'rutina': rutina, 'alumno':alum, 'mensaje':mensaje})
                #Usted no puede inscribirse a la rutina      porque pertenece a la rutina     
        else:
            if request.method == 'POST':
                fichaForm = FichaForm(request.POST)
                alumnoForm = AlumnoForm(request.POST)
                peticion = request.POST.copy()
                print(peticion)
                entrenamiento = peticion.pop('entrenamiento')
                entrenamiento = entrenamiento[0]
                
                altura = peticion.pop('altura')
                altura = altura[0]
                
                peso = peticion.pop('peso')
                peso = peso[0]
                
                if entrenamiento == "profesor":
                    try:
                        disp = peticion.pop('disponibilidad')
                    except:
                        
                        error = "\n Debe seleccionar los dias y horarios en los que desea entrenar."
                        print(error)
                        return render (request, 'rutina/inscribirseRutina.html', {'ficha':fichaForm, 'alumno':alumnoForm, 'rutina':rutina, 'disponibilidad':disponibilidad, 'dias':dias, 'error':error})
                else:
    
                    try:
                        dias = peticion.pop('dias')
                    except:
                        
                        error = "\n Debe seleccionar los dias y horarios en los que desea entrenar."
                        return render (request, 'rutina/inscribirseRutina.html', {'ficha':fichaForm, 'alumno':alumnoForm, 'rutina':rutina, 'disponibilidad':disponibilidad, 'dias':dias, 'error':error})
                
                
                
                if entrenamiento == "sistema":
                    actividad = peticion.pop('actividad')
                    actividad = actividad[0]
                    circu = peticion.pop('circu')
                    circu = circu[0]
                
                sexo = peticion.pop('sexo')
                sexo = sexo[0]
                
                
                
                if fichaForm.is_valid() and alumnoForm.is_valid():
                    alumno = alumnoForm.save(commit=False)
                    ficha = fichaForm.save(commit=False)
                    alumno.user = user
                    alumno.rutina_id = rutina
                    alumno.profesor_id = rutina.profesor_id
                    alumno.nombre = user.first_name
                    alumno.apellido = user.last_name
                    alumno.email = user.email
                    if entrenamiento == 'profesor':
                        alumno.nivel_id = None
                        alumno.entrenamiento_sistema = False
                        
                        
                        
                    else:
                        nivel = calcularNivel(altura, circu, peso, actividad, sexo)
                        nivel = nivel.capitalize()
                        print(nivel)
                        alumno.nivel_id = Nivel.objects.get(nombre = nivel)
                        alumno.entrenamiento_sistema = True       
                    
                    alumno.save() 
                    if entrenamiento == 'sistema':
                        alumno.semana_id.set(dias)  
                        
                    
                    if entrenamiento == 'profesor':
                        for d in disp:
                            DisponibilidadProfesor.objects.filter(id=int(d)).update(alumno_id=alumno, ocupado=True)
                            
                    grupo = Group.objects.get(name='Alumno') 
                    grupo.user_set.add(user)        
                    ficha.alumno_id = alumno
                    ficha.circunferenciaMuneca = circu
                    ficha.save()
                    return render (request, 'rutina/inscripcionExitosa.html', {'alumno':Alumno.objects.get(user_id=user.id), 'rutina':rutina})
            else:
                fichaForm = FichaForm()
                alumnoForm = AlumnoForm()
    return render (request, 'rutina/inscribirseRutina.html', {'ficha':fichaForm, 'alumno':alumnoForm, 'rutina':rutina, 'disponibilidad':disponibilidad, 'dias':dias})
    return redirect ('/rutinas/')
    
"""  
si es staff renderizo el template
sino
    si es profesor renderizo el template
    sino
        si es alumno
            si ya tiene rutina renderizo el template
            sino le permito
"""
                
    
    
            
    
    
    
    
    
    
    
    
