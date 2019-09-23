from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, UsuarioForm, LoginForm, DisponibilidadForm
from django.views.generic import TemplateView
from apps.rutina.views import ListadoRutinas
from django.contrib.auth.models import User, Permission
from django.views.generic.edit import FormView
from django.urls import reverse_lazy 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Profesor, Alumno, FichaAlumno, Semana, DisponibilidadProfesor
from ..rutina.models import Rutina, Nivel

"""import os
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, cm
from django.http import HttpResponse"""


# Create your views here.
class Home(TemplateView):
    template_name = "home/home.html"
    
class Administrar(PermissionRequiredMixin,TemplateView):
    permission_required = ('rutina.view_actividad')
    template_name = "home/administracion.html"
    
class PaginaInicial(TemplateView):
    template_name = "home/paginaInicial.html"
    
def listadoAlumnos(request, pk):
    user = User.objects.get(id=pk)
    rutinas = Rutina.objects.filter(estado=True)
    if (Profesor.objects.filter(user_id=user.id).exists()):
        profesor = Profesor.objects.get(user_id=pk)
    else:
        return redirect('/home')
    
    if request.method == 'GET':  
        if (Alumno.objects.filter(profesor_id=profesor.id).exists()):
            alumnos = Alumno.objects.filter(profesor_id=profesor.id)
            for alumno in alumnos:
                alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
            mensaje = None
        else:
            mensaje = "Usted no tiene alumnos a cargo"
            
        return render(request, 'rutina/listadoAlumnos.html', {'profesor' : profesor, 'mensaje' : mensaje, 'alumnos' : alumnos, 'rutinas':rutinas})
    
    if request.method == 'POST':
        peticion = request.POST.copy()
        print(peticion)
        
        
        rutinas = peticion.pop('rutinas')
        rutinas = rutinas[0]
        
        entrenamiento = peticion.pop('entrenamiento')
        entrenamiento = entrenamiento[0]
        
        nivel = peticion.pop('nivel')
        nivel = nivel[0]
        
        if (Profesor.objects.filter(user_id=user.id).exists()):
            profesor = Profesor.objects.get(user_id=pk)
        else:
            return redirect('/home')
        
        if (Alumno.objects.filter(profesor_id=profesor.id).exists()):
            if rutinas != "Rutinas" and entrenamiento != "Tipo entrenamiento" and nivel != "Nivel":
                if entrenamiento == "profesor":
                    ruti = Rutina.objects.get(nombre=rutinas)
                    niv = Nivel.objects.get(nombre=nivel)
                    alumnos = Alumno.objects.filter(profesor_id=profesor.id, rutina_id=ruti.id, entrenamiento_sistema=False, nivel_id=None)
                    for alumno in alumnos:
                        alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
                    mensaje = None
                else:
                    ruti = Rutina.objects.get(nombre=rutinas)
                    niv = Nivel.objects.get(nombre=nivel)
                    alumnos = Alumno.objects.filter(profesor_id=profesor.id, rutina_id=ruti.id, entrenamiento_sistema=True, nivel_id=niv.id)
                    for alumno in alumnos:
                        alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
                    mensaje = None
                    
                
            if rutinas != "Rutinas" and entrenamiento != "Tipo entrenamiento" and nivel == "Nivel":
                if entrenamiento == "profesor":
                    ruti = Rutina.objects.get(nombre=rutinas)
                    alumnos = Alumno.objects.filter(profesor_id=profesor.id, rutina_id=ruti.id, entrenamiento_sistema=False)
                    for alumno in alumnos:
                        alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
                    mensaje = None
                else:
                    ruti = Rutina.objects.get(nombre=rutinas)
                    alumnos = Alumno.objects.filter(profesor_id=profesor.id, rutina_id=ruti.id, entrenamiento_sistema=True)
                    for alumno in alumnos:
                        alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
                    mensaje = None
                    
                
            if rutinas != "Rutinas" and entrenamiento == "Tipo entrenamiento" and nivel == "Nivel":
                ruti = Rutina.objects.get(nombre=rutinas)
                alumnos = Alumno.objects.filter(profesor_id=profesor.id, rutina_id=ruti.id)
                for alumno in alumnos:
                    alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
                mensaje = None
                
                
            if rutinas != "Rutinas" and entrenamiento == "Tipo entrenamiento" and nivel != "Nivel":
                ruti = Rutina.objects.get(nombre=rutinas)
                niv = Nivel.objects.get(nombre=nivel)
                alumnos = Alumno.objects.filter(profesor_id=profesor.id, rutina_id=ruti.id, nivel_id=niv.id)
                for alumno in alumnos:
                    alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
                mensaje = None
                
            
            if rutinas == "Rutinas" and entrenamiento == "Tipo entrenamiento" and nivel == "Nivel":
                alumnos = Alumno.objects.filter(profesor_id=profesor.id)
                for alumno in alumnos:
                    alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
                mensaje = None
                
            
            if rutinas == "Rutinas" and entrenamiento != "Tipo entrenamiento" and nivel == "Nivel":
                if entrenamiento == "profesor":
                    alumnos = Alumno.objects.filter(profesor_id=profesor.id, entrenamiento_sistema=False)
                    for alumno in alumnos:
                        alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
                    mensaje = None
                else:
                    alumnos = Alumno.objects.filter(profesor_id=profesor.id, entrenamiento_sistema=True)
                    for alumno in alumnos:
                        alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
                    mensaje = None
                    
                    
            if rutinas == "Rutinas" and entrenamiento != "Tipo entrenamiento" and nivel != "Nivel":
                if entrenamiento == "profesor":
                    alumnos = Alumno.objects.filter(profesor_id=profesor.id, entrenamiento_sistema=False)
                    for alumno in alumnos:
                        alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
                    mensaje = None
                else:
                    niv = Nivel.objects.get(nombre=nivel)
                    alumnos = Alumno.objects.filter(profesor_id=profesor.id, entrenamiento_sistema=True, nivel_id=niv.id)
                    for alumno in alumnos:
                        alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
                    mensaje = None
                    
            
            
            if rutinas == "Rutinas" and entrenamiento == "Tipo entrenamiento" and nivel != "Nivel":
                niv = Nivel.objects.get(nombre=nivel)
                alumnos = Alumno.objects.filter(profesor_id=profesor.id, nivel_id=niv.id) 
                for alumno in alumnos:
                    alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
                mensaje = None           
                              
        else:
            mensaje = "Usted no tiene alumnos a cargo"
            
        rutinas = Rutina.objects.filter(estado=True)
        return render(request, 'rutina/listadoAlumnos.html', {'profesor' : profesor, 'mensaje' : mensaje, 'alumnos' : alumnos, 'rutinas':rutinas})         
        
"""def reporte (request, alumnos):
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'attachment: filename=Listado.pdf'
     
     buffer = BytesIO()
     c = Canvas.Canvas(buffer, pagesize=A4)
     
     #header
     c.setLineWidth(.3)
     c.setFont('Helvetica', 22)
     c.drawString(30,750,'FitRou')
     c.setFont('Helvetica', 12)
     c.drawString(30,735,'Listado de alumnos')
     
     c.setFont('Helvetica-Bold',12)
     c.drawString(480,750,"21/09/2019")
     c.line(460,747,560,747)
     
     estudiantes = [(alumno.nombre,alumno.fecha_nac, alumno.rutina_id, alumno.nivel_id) for alumno in alumnos]
     
     
     #Table header
     styles = getSampleStyleSheet()
     styleBH = styles["Normal"]
     styleBH.alignment = TA_CENTER
     styleBH.fontSize = 10
     
     nombre = Paragraph('''Nombre''',styleBH)
     fecha_nac = Paragraph(''''Fecha de nac.''',styleBH)
     rutina = Paragraph('''Rutina''',styleBH)
     nivel = Paragraph(''''Nivel''',styleBH)
     
     data = [[nombre,fecha_nac,rutina,nivel]]
     
     styles = getSampleStyleSheet()
     styleN = styles["BodyText"]
     styleN.alignment = TA_CENTER
     styleN.fontSize = 7
     
     width, height = A4
     high = 650
     """
     

def registro(request):               
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():

            user = form.save()
            dj_login(request, user)
            permission = Permission.objects.get(name='Can view Rutina')
            user.user_permissions.add(permission)
            user.save()
            return redirect ('/home')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")

    form = NewUserForm
    return render(request, 'registro.html', context={'form': form})
    

def login (request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                dj_login(request, user)
                messages.info(request, f"Te has logueado como {username}")
                return redirect ('/home')
            else:
                messages.error(request, "Nombre o contraseña invalidos")
        else:
            messages.error(request, "Nombre o contraseña invalidos")
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


#Esto no se va a usar
def cargarDatosUsuario(request):
    if request.method == 'POST':
        userForm = UsuarioForm(request.POST)
        if userForm.is_valid():
            userForm.save()
            return redirect ('/home')
    else:
        userForm = UsuarioForm()
        return render(request, 'cargarDatos.html', {'userForm':userForm})
    
    
class Login(FormView):
    template_name='login.html'
    form_class = LoginForm
    succes_url = reverse_lazy('/home')
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    
    def dispath(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url)
        else:
            return super(Login,self).dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        dj_login(self.request,form.get_user())
        return super(Login,self).form_valid(form)
        
        
def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


def agregarDisponibilidad(request, pk):
    if (not (Profesor.objects.filter(user_id=pk).exists())):
        return redirect ('/home/administracion')
    else:
        profesor = Profesor.objects.get(user_id=pk)
        dias = Semana.objects.all()
    
    
    if request.method == 'POST':
        peticion = request.POST.copy()
        print(peticion)
        dias = peticion.pop('dias')
        hora_inicio = peticion.pop('horario_inicio')
        hora_inicio = hora_inicio[0]
        
        hora_final = peticion.pop('horario_final')
        hora_final = hora_final[0]
        
        print(hora_inicio + ' - ' + hora_final)
        disponibilidadForm = DisponibilidadForm(request.POST)
        if disponibilidadForm.is_valid():
            if (hora_inicio<hora_final):
                i=0
                while i < len(dias):
                    semana = Semana.objects.get(dia=dias[i])
                    disponibilidad = DisponibilidadProfesor.objects.create(horario_inicio=hora_inicio, semana_id=semana, profesor_id=profesor, horario_final=hora_final)
                    disponibilidad.save()
                    i+=1
                mensaje = None
                return redirect('/home/administracion')
            else:
                mensaje = "El horario final no puede ser menor al horario de inicio."
                return render(request, 'rutina/agregarDisponibilidad.html',{'disponibilidadForm':disponibilidadForm, 'dias':dias, 'mensaje':mensaje})
            
            
    else:
        disponibilidadForm = DisponibilidadForm()
        mensaje = None
        return render(request, 'rutina/agregarDisponibilidad.html',{'disponibilidadForm':disponibilidadForm, 'dias':dias, 'mensaje':mensaje})
    
    return redirect ('/home/administracion/')