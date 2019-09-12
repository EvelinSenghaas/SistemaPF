from django.shortcuts import render, redirect
from .models import Rutina, Actividad, Detalle
from ..home.models import Alumno, FichaAlumno, Profesor
from ..home.forms import AlumnoForm, FichaForm
from .forms import DetalleForm, ActividadForm, RutinaForm
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from apps.home.models import Profesor
from django.contrib.auth.models import User
import operator

# Create your views here.
    
class Rutinas (PermissionRequiredMixin,ListView):
    permission_required = ('rutina.view_rutina', 'rutina.add_rutina')
    template_name = 'rutina/administrarRutinas.html'
    context_object_name = 'rutinas'
    queryset = Rutina.objects.filter(estado=True)
    


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
    for a in det:
        i=0
        detalles += Detalle.objects.filter(id=a[i], estado=True)
        i+=1
    return render (request, 'rutina/verActividad.html', { 'actividad': actividad, 'detalles':detalles})
       

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
    template_name = 'rutina/agregarActividad.html'
    form_class = ActividadForm
    succes_name = reverse_lazy('/rutinas/actividades/')
    
def agregarActividad(request):
    detalle = Detalle.objects.filter(estado=True)
    if request.method == 'POST':
        actividadForm = ActividadForm(request.POST)
        peticion = request.POST.copy()
        det = peticion.pop('detalle')
        if actividadForm.is_valid():
            actividad = actividadForm.save(commit=False)
            actividad.save()
            for a in det:
                actividad.detalle_id.add(a)     
            actividad.save()
            return redirect('/rutinas/actividades/')     
    else:
        actividadForm = ActividadForm()
        return render(request, 'rutina/agregarActividad.html',{'actividadForm':actividadForm,'detalle':detalle})
    return redirect('/rutinas/actividades/')  
        

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
        if rutinaForm.is_valid():
            rutina = rutinaForm.save(commit=False)
            rutina.profesor_id=profesor
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
    succes_url = reverse_lazy('/rutinas')
    

class EditarActividad(PermissionRequiredMixin,UpdateView):
    permission_required = 'rutina.change_actividad'
    model = Actividad
    template_name = 'rutina/agregarActividad.html'
    actividadForm = ActividadForm
    succes_url = reverse_lazy('/rutinas')
    
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
        object.estado = not(object.estado)
        object.save()
        return redirect('/rutinas/administrar_rutinas')
    
class EliminarActividad(DeleteView):
    
    model = Actividad
    def post(self,request, pk, *args, **kwargs):
        object = Actividad.objects.get(id = pk)
        object.estado = not(object.estado)
        object.save()
        return redirect('/rutinas/actividades')
    
class EliminarDetalle(DeleteView):
    
    model = Detalle

    def post(self,request, pk, *args, **kwargs):
        object = Detalle.objects.get(id = pk)
        object.estado = not(object.estado)
        object.save()
        return redirect('/rutinas/administrar_detalles')
    
    
def inscribirseRutina(request, pk1, pk2):
    #Identificamos al user que se quiere inscribir (pk es de usuario)
    user = User.objects.get(id = pk1)
    #Identificamos la rutina a la que se quiere inscribir
    rutina = Rutina.objects.get(id = pk2)    
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
                if fichaForm.is_valid() and alumnoForm.is_valid():
                    alumno = alumnoForm.save(commit=False)
                    ficha = fichaForm.save(commit=False)
                    alumno.user = user
                    alumno.rutina_id = rutina
                    alumno.profesor_id = rutina.profesor_id
                    alumno.save()            
                    ficha.alumno_id = alumno
                    ficha.save()
                    return redirect ('/rutinas/')
            else:
                fichaForm = FichaForm()
                alumnoForm = AlumnoForm()
    return render (request, 'rutina/inscribirseRutina.html', {'ficha':fichaForm, 'alumno':alumnoForm})
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
                
    
    
            
    
    
    
    
    
    
    
    
