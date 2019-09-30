from django.shortcuts import render, redirect
from .models import Rutina, Actividad, Detalle, Nivel, Repeticion
from ..home.models import Alumno, FichaAlumno, Profesor, Semana, DisponibilidadProfesor
from ..home.forms import AlumnoForm, FichaForm
from .forms import DetalleForm, ActividadForm, RutinaForm, NivelForm, RepeticionForm
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from apps.home.models import Profesor
from django.contrib.auth.models import User
import operator
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.core import serializers


from django.utils import timezone
import time
import calendar
from datetime import datetime, date


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
    
def verClase(request, pk):
    user = User.objects.get(id=pk)
    if (Alumno.objects.filter(user_id=user.id).exists()):
        alumno = Alumno.objects.get(user_id=user.id)
        profesor = alumno.profesor_id
        
        
        if request.method == 'GET':
            disponibilidad = DisponibilidadProfesor.objects.filter(alumno_id=alumno.id)
            
            now = datetime.now()
            dia = now.strftime("%A")
            dia = traducirDia(dia)
            
            
            diasAlumno=[]
            for disp in disponibilidad:
                diasAlumno.append(Semana.objects.get(dia=disp.semana_id))
            
            clase=None
            for diaAlumno in diasAlumno:    
                if dia == diaAlumno.dia:
                    mensaje = None
                    hora_inicio = DisponibilidadProfesor.objects.get(alumno_id=alumno.id, semana_id=diaAlumno).horario_inicio
                    hora_final = DisponibilidadProfesor.objects.get(alumno_id=alumno.id, semana_id=diaAlumno).horario_final
                    
                    if now.time() < hora_inicio:
                        clase = "Tienes una clase con " + str(alumno.profesor_id)  + " hoy desde las " + hora_inicio.strftime("%H:%M") + " hasta las " + hora_final.strftime("%H:%M") +"hs."
                    
                    if  hora_inicio <= now.time() <= hora_final:
                        clase = "La clase con " + str(alumno.profesor_id)  + " esta en curso. "
                    
                    if now.time() > hora_final:
                        clase = None
                        mensaje = "Tu clase con " + str(alumno.profesor_id) + " ya ha terminado."
                        break
                    break
                    
                if dia != diaAlumno.dia:
                    mensaje = "Hoy no es día de entrenamiento, debes esperar para tu siguiente clase "
                    
            return render (request, 'rutina/clases.html', {'alumno':alumno, "mensaje":mensaje, 'disponibilidad':disponibilidad, 'clase':clase, 'profesor':profesor})
        
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
        alumno = Alumno.objects.get(user_id=pk)
        edad = alumno.edad(alumno.fecha_nac)
        ficha = FichaAlumno.objects.get(alumno_id=alumno.id)
        mensaje = None
    else:
        mensaje = "El alumno no existe"
        return redirect('/home/')
    
    return render (request, 'home/verPerfil.html', { 'alumno': alumno, 'mensaje':mensaje, 'ficha':ficha, 'edad':edad})
    
    
def verRutina(request, pk):
    rutina = Rutina.objects.get(id = pk)
    actividades = []
    act = Rutina.objects.values_list('actividad_id').filter(id=pk)
    for a in act:
        i=0
        actividades += Actividad.objects.filter(id=a[i], estado=True)
        i+=1
    return render (request, 'rutina/verRutina.html', { 'rutina': rutina, 'actividades':actividades})


def verActividad(request, pk):
    actividad = Actividad.objects.get(id = pk)
    detalles = []
    det = Actividad.objects.values_list('detalle_id').filter(id=pk)
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
class AgregarDetalle(PermissionRequiredMixin, CreateView):
    permission_required = 'rutina.add_detalle'
    model = Detalle
    form_class = DetalleForm
    template_name = 'rutina/agregarDetalle.html'
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
    
    
def agregarActividad(request):
    nivel = Nivel.objects.all() 
    error = None
    if request.method == 'POST':
        form = ActividadForm(request.POST)
        form2 = RepeticionForm(request.POST)
        
        peticion = request.POST.copy()
        nivel_id = peticion.pop('nivel_id')
        
        
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
            repeticion = form2.save(commit=False)
            acti = Actividad.objects.get(id=actividad.id)  
            i=0
            while i < len(nivel_id):
                r = Repeticion.objects.create(actividad_id = actividad, nivel_id = Nivel.objects.get(id = nivel_id[i]), repeticionesMinimas = rep_min[i])
                r.save()
                i+=1
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
        nivel_id = peticion.pop('nivel_id')
        rep_min = peticion.pop('repeticionesMinimas')
        
        print(nivel_id)
        
        if form.is_valid() and form2.is_valid():
            actividad = form.save()
            form2.actividad_id = form
            form2.save(commit=False)
        i=0
        while i < len(nivel_id):
            Repeticion.objects.filter(actividad_id = actividad.id, nivel_id = nivel_id[i]).update(nivel_id = Nivel.objects.get(id = nivel_id[i]))
            Repeticion.objects.filter(actividad_id = actividad.id, nivel_id = nivel_id[i]).update(repeticionesMinimas = rep_min[i])
            i+=1
            
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
        actividades = peticion.pop('actividad_id')
        print(request.POST)
        if rutinaForm.is_valid():
            rutina = rutinaForm.save(commit=False)
            rutina.profesor_id=profesor
            rutina.save()
            for act in actividades:
                rutina.actividad_id.add(act)
            rutina.save()
            return redirect ('/rutinas/administrar_rutinas/')
    else:
        rutinaForm = RutinaForm()
        return render(request, 'rutina/agregarRutina.html',{'rutinaForm':rutinaForm})
    
    return redirect ('/rutinas/administrar_rutinas/')
 
#Editar    
class EditarRutina(PermissionRequiredMixin,UpdateView):
    permission_required = 'rutina.change_rutina'
    model = Rutina
    template_name = 'rutina/agregarRutina.html'
    form_class = RutinaForm
    succes_url = reverse_lazy('/rutinas/administrar_rutinas')
    

class EditarActividad(PermissionRequiredMixin,UpdateView):
    permission_required = 'rutina.change_actividad'
    model = Actividad
    template_name = 'rutina/agregarActividad.html'
    form_class = ActividadForm
    succes_url = reverse_lazy('/rutinas/actividades/')
    
class EditarDetalle(PermissionRequiredMixin,UpdateView):
    permission_required = 'rutina.change_detalle'
    model = Detalle
    template_name = 'rutina/agregarDetalle.html'
    form_class = DetalleForm
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
    
class EliminarActividad(DeleteView):
    model = Actividad
    def post(self,request, pk, *args, **kwargs):
        object = Actividad.objects.get(id = pk)
        if (Rutina.objects.filter(actividad_id=object.id).exists()):
            mensaje = "Usted no puede borrar " + object.nombre + " porque ya pertenece a una rutina"
            return render(request, 'rutina/errorEliminacion.html',{'object':object, 'mensaje':mensaje})
        else:
            Actividad.objects.get(id = object.id).delete()
        return redirect('/rutinas/actividades')
    
class EliminarDetalle(DeleteView):
    model = Detalle
    def post(self,request, pk, *args, **kwargs):
        object = Detalle.objects.get(id = pk)
        if (Actividad.objects.filter(detalle_id=object.id).exists()):
            mensaje = "Usted no puede borrar " + object.musculo + " porque ya pertenece a una actividad"
            return render(request, 'rutina/errorEliminacion.html',{'object':object, 'mensaje':mensaje})
        else:
            Detalle.objects.get(id = object.id).delete()
        return redirect('/rutinas/administrar_detalles')
    
#Metodo para calcular el nivel a asignar al alumno
def calcularNivel(altura, circu, peso, actividad, sexo):
    
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
    
    disponibilidad = DisponibilidadProfesor.objects.filter(profesor_id=rutina.profesor_id, ocupado=False)
    """dias = []
    for i in Semana.objects.all():
        if DisponibilidadProfesor.objects.filter(semana_id=i, ocupado=False).exists():
            dias.append(i)"""
            
    
       
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
                
                disp = peticion.pop('disponibilidad')
                
                
                
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
                        alumno.nivel_id = Nivel.objects.get(nombre = nivel)
                        alumno.entrenamiento_sistema = True                   
                    alumno.save()   
                    
                    if entrenamiento == 'profesor':
                        for d in disp:
                            DisponibilidadProfesor.objects.filter(id=int(d)).update(alumno_id=alumno, ocupado=True)
                            
                    grupo = Group.objects.get(name='Alumno') 
                    grupo.user_set.add(user)        
                    ficha.alumno_id = alumno
                    ficha.save()
                    return render (request, 'rutina/inscripcionExitosa.html', {'alumno':Alumno.objects.get(user_id=user.id), 'rutina':rutina})
            else:
                fichaForm = FichaForm()
                alumnoForm = AlumnoForm()
    return render (request, 'rutina/inscribirseRutina.html', {'ficha':fichaForm, 'alumno':alumnoForm, 'rutina':rutina, 'disponibilidad':disponibilidad})
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
                
    
    
            
    
    
    
    
    
    
    
    
