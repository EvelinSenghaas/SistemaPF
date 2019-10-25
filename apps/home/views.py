# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, UsuarioForm, LoginForm, DisponibilidadForm
from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView
from apps.rutina.views import ListadoRutinas
from django.contrib.auth.models import User, Permission
from django.views.generic.edit import FormView
from django.urls import reverse_lazy 
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from .models import Profesor, Alumno, FichaAlumno, Semana, DisponibilidadProfesor
from ..rutina.models import Rutina, Nivel
import sweetify


from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

import time
from datetime import datetime

from io import BytesIO

from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, mm
from reportlab.platypus import Table
from reportlab.lib.enums import TA_CENTER


# Create your views here.
class Home(TemplateView):
    template_name = "home/home.html"
    
class Administrar(PermissionRequiredMixin,TemplateView):
    permission_required = ('rutina.view_actividad')
    template_name = "home/administracion.html"
    
class PaginaInicial(TemplateView):
    template_name = "home/paginaInicial.html"
    
#No se usa    
class EditarDisponibilidad(PermissionRequiredMixin,UpdateView):
    permission_required = 'rutina.change_detalle'
    model = DisponibilidadProfesor
    template_name = 'rutina/agregarDisponibilidad.html'
    form_class = DisponibilidadForm
    succes_url = reverse_lazy('/rutinas/administracion')
    
    
def editarDisponibilidad(request, pk):
    disponibilidad = DisponibilidadProfesor.objects.get(id=pk)
    profesor = Profesor.objects.get(id=disponibilidad.profesor_id.id)
    dias = Semana.objects.all()
    print(profesor)
    
    if request.method == 'GET':
        form = DisponibilidadForm(instance = disponibilidad) 
        print()
        dias = Semana.objects.exclude(dia=disponibilidad.semana_id) 
        diaSelec = disponibilidad.semana_id
        mensaje = None
        return render(request, 'rutina/agregarDisponibilidad.html',{'form':form, 'dias':dias, 'diaSelec':diaSelec, 'mensaje':mensaje})
    else:
        peticion = request.POST.copy()
        print(peticion)
        
        form = DisponibilidadForm(request.POST, instance = disponibilidad)
        try:
            dias = peticion.pop('dias')
        except:
            mensaje = "No ha seleccionado los dias."
            return render(request, 'rutina/agregarDisponibilidad.html',{'form':form, 'mensaje':mensaje}) 
            
        diaSelec = disponibilidad.semana_id
        
        
        
        try:
            inicio = peticion.pop('horario_inicio')
            hora_inicio = datetime.strptime(inicio[0], "%H:%M:%S").time()
               
            final = peticion.pop('horario_final')
            hora_final = datetime.strptime(final[0], "%H:%M:%S").time()
        except:
            mensaje = "Por favor ingrese correctamente el horario en el formato especificado (HH:MM:SS)"
            disp = disponibilidad.id
            return render(request, 'rutina/agregarDisponibilidad.html',{'form':form, 'dias':dias, 'diaSelec':diaSelec, 'mensaje':mensaje, 'disp':disp}) 
        
        
        print(hora_inicio)
        #print(disponibilidad.horario_inicio)
        print(hora_final)
        
        #Controlamos que no exista esa disponibilidad
        for d in dias:
            print(d)
            if (DisponibilidadProfesor.objects.filter(semana_id=Semana.objects.get(dia=d).id, horario_inicio=hora_inicio, horario_final=hora_final).exists()):
                mensaje = "La disponibilidad ingresada ya existe."
                return render(request, 'rutina/agregarDisponibilidad.html',{'form':form, 'dias':dias, 'diaSelec':diaSelec, 'mensaje':mensaje})
        
        if form.is_valid():
            form = form.save()
            if diaSelec.dia in dias:
                if (hora_inicio<hora_final):
                    i=0
                    while i < len(dias):
                        
                        semana = dias[i]
                        if (semana == diaSelec.dia):                    
                            DisponibilidadProfesor.objects.filter(id=disponibilidad.id, horario_inicio=disponibilidad.horario_inicio, horario_final=disponibilidad.horario_final, ocupado=False).update(semana_id=Semana.objects.get(dia=semana).id)
                            
                            DisponibilidadProfesor.objects.filter(id=disponibilidad.id, horario_inicio=disponibilidad.horario_inicio, horario_final=disponibilidad.horario_final, ocupado=False).update(horario_inicio=hora_inicio)
                            
                            DisponibilidadProfesor.objects.filter(id=disponibilidad.id, horario_inicio=disponibilidad.horario_inicio, horario_final=disponibilidad.horario_final, ocupado=False).update(horario_final=hora_final)
                            i+=1
                        else:
                            disp = DisponibilidadProfesor.objects.create(horario_inicio=hora_inicio, horario_final=hora_final, semana_id=Semana.objects.get(dia=semana), profesor_id=Profesor.objects.get(id=profesor.id))
                            disp.save()
                            i+=1
                        
                    mensaje = None
                    messages.success(request, "Disponibilidad modificada con éxito.")
                else:
                    mensaje = "El horario final no puede ser menor al horario de inicio."
                    return render(request, 'rutina/agregarDisponibilidad.html',{'form':form, 'dias':dias, 'diaSelec':diaSelec, 'mensaje':mensaje}) 
            else:
                if (hora_inicio<hora_final):
                    i=0
                    while i < len(dias):
                        
                        semana = dias[i]
                        if (semana == diaSelec.dia):                    
                            DisponibilidadProfesor.objects.filter(id=disponibilidad.id, horario_inicio=disponibilidad.horario_inicio, horario_final=disponibilidad.horario_final, ocupado=False).update(semana_id=Semana.objects.get(dia=semana).id)
                            
                            DisponibilidadProfesor.objects.filter(id=disponibilidad.id, horario_inicio=disponibilidad.horario_inicio, horario_final=disponibilidad.horario_final, ocupado=False).update(horario_inicio=hora_inicio)
                            
                            DisponibilidadProfesor.objects.filter(id=disponibilidad.id, horario_inicio=disponibilidad.horario_inicio, horario_final=disponibilidad.horario_final, ocupado=False).update(horario_final=hora_final)
                            i+=1
                        else:
                            disp = DisponibilidadProfesor.objects.create(horario_inicio=hora_inicio, horario_final=hora_final, semana_id=Semana.objects.get(dia=semana), profesor_id=Profesor.objects.get(id=profesor.id))
                            disp.save()
                            i+=1
                        
                    mensaje = None
                    messages.success(request, "Disponibilidad modificada con éxito.")
                else:
                    mensaje = "El horario final no puede ser menor al horario de inicio."
                    return render(request, 'rutina/agregarDisponibilidad.html',{'form':form, 'dias':dias, 'diaSelec':diaSelec, 'mensaje':mensaje})
                
                
        else:
            error = form.errors
            mensaje = None
            return render(request, 'rutina/agregarDisponibilidad.html',{'form':form, 'dias':dias, 'diaSelec':diaSelec, 'mensaje':mensaje}) 
            

    
    return redirect('/home/administrar_disponibilidad/'+str(profesor.user_id))
     
           
#No se usa mas
class EliminarDisponibilidad(DeleteView):
    model = DisponibilidadProfesor
    def post(self,request, pk, *args, **kwargs):
        object = DisponibilidadProfesor.objects.get(id = pk)
        if not (DisponibilidadProfesor.objects.filter(id=object.id, ocupado=False).exists()):
            mensaje = "Usted no puede deshabilitar este horario debido a que el mismo se encuentra ocupado por el alumno/a " + str(object.alumno_id)
            return render(request, 'rutina/errorEliminacion.html',{'object':object, 'mensaje':mensaje})
        else:
            DisponibilidadProfesor.objects.get(id = object.id).delete()
        return redirect('/home/administracion')       


def eliminarDisponibilidad(request, pk):
    disp = DisponibilidadProfesor.objects.get(id = pk)
    print(request) 
    if not (DisponibilidadProfesor.objects.filter(id=disp.id, ocupado=False).exists()):
            messages.error(request, "Usted no puede deshabilitar este horario debido a que el mismo se encuentra ocupado por el alumno/a " + str(disp.alumno_id)+".")
            
    else:
        DisponibilidadProfesor.objects.get(id = disp.id).delete()
        messages.success(request, "Disponibilidad eliminada con éxito.")  
    return redirect('/home/administrar_disponibilidad/'+str(disp.profesor_id.user_id)) 


    
def listadoDisponibilidad (request,pk):
    user = User.objects.get(id = pk)
    profesor = Profesor.objects.get(user_id=user.id)
    
    if request.method == 'GET':
        disponibilidad = DisponibilidadProfesor.objects.filter(profesor_id=profesor.id)
        print(disponibilidad)
        return render(request, 'rutina/administrarDisponibilidad.html', {'disponibilidad':disponibilidad})
    else:
        return redirect ('/home/administrar_disponibilidad/')
    
    
    
#Esta funcion se usa para filtrar la tabla de alumnos    
def filtrar(rutinas, entrenamiento, nivel, profesor): 
    if rutinas != "Rutinas" and entrenamiento != "Tipo entrenamiento" and nivel != "Nivel":
        print('entro')
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
        print('entro')
        ruti = Rutina.objects.get(nombre=rutinas)
        alumnos = Alumno.objects.filter(profesor_id=profesor.id, rutina_id=ruti.id)
        for alumno in alumnos:
            alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
        mensaje = None
                
                
    if rutinas != "Rutinas" and entrenamiento == "Tipo entrenamiento" and nivel != "Nivel":
        print('entro')
        ruti = Rutina.objects.get(nombre=rutinas)
        niv = Nivel.objects.get(nombre=nivel)
        alumnos = Alumno.objects.filter(profesor_id=profesor.id, rutina_id=ruti.id, nivel_id=niv.id)
        for alumno in alumnos:
            alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
        mensaje = None
                
            
    if rutinas == "Rutinas" and entrenamiento == "Tipo entrenamiento" and nivel == "Nivel":
        print('entro')
        alumnos = Alumno.objects.filter(profesor_id=profesor.id)
        for alumno in alumnos:
            alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
        mensaje = None
                
            
    if rutinas == "Rutinas" and entrenamiento != "Tipo entrenamiento" and nivel == "Nivel":
        print('entro')
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
        print('entro')
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
        print('entro')
        niv = Nivel.objects.get(nombre=nivel)
        alumnos = Alumno.objects.filter(profesor_id=profesor.id, nivel_id=niv.id) 
        for alumno in alumnos:
            alumno.fecha_nac = alumno.edad(alumno.fecha_nac)
        mensaje = None     
            
    return alumnos


def reporte (request, alumnos):
     response = HttpResponse(content_type='application/pdf')
     response['Content-Disposition'] = 'attachment: filename=Listado_alumnos.pdf'
     
     buffer = BytesIO()
     c = canvas.Canvas(buffer, pagesize=A4)
     
     peticion = request.POST.copy()
     rutina = peticion.pop('rutinas')
     entrenamiento = peticion.pop('entrenamiento')
     nivel = peticion.pop('nivel')
         
                 

     
     
     #header
     c.setLineWidth(.3)
     c.setFont('Times-Bold', 22)
     c.drawString(30,750,'FitRou')
     c.setFont('Times-Bold', 12)
     
     c.drawString(30,730,'Listado de alumnos filtrado por ' + str(rutina[0])+', '+str(entrenamiento[0])+' y '+str(nivel[0])+':')
     
     fecha = str(time.strftime("Fecha: %d/%m/%y"))
     c.setFont('Times-Roman',10)
     c.drawString(475,750,fecha)
     
     profesor = alumnos[0].profesor_id
     profe = str("Profesor: " + str(profesor))
     c.setFont('Times-Roman',10)
     c.drawString(475,735,profe)
     
     
     
     """estudiantes = [(alumno.nombre,alumno.fecha_nac, alumno.rutina_id, alumno.nivel_id) for alumno in alumnos]"""
     
     
     #Table header
     styles = getSampleStyleSheet()
     styleBH = styles["Normal"]
     styleBH.alignment = TA_CENTER
     styleBH.fontSize = 10
     
     
     
     
     nombre = Paragraph('''Nombre y apellido''',styleBH)
     fecha_nac = Paragraph('''Edad''',styleBH)
     rutina = Paragraph('''Rutina''',styleBH)
     entrenamiento = Paragraph('''Entrenamiento''',styleBH)
     nivel = Paragraph('''Nivel''',styleBH)
     
     data = [[nombre,fecha_nac,rutina,entrenamiento,nivel]]
     
     styles = getSampleStyleSheet()
     styleN = styles["BodyText"]
     styleN.alignment = TA_CENTER
     styleN.fontSize = 7
     
     width, height = A4
     high = 550
     
     for alumno in alumnos:
         if alumno.entrenamiento_sistema == True:
             alumno.entrenamiento_sistema = "Sistema"
         else:
             alumno.entrenamiento_sistema = "Profesor"
     for alumno in alumnos:
         this_student = [ alumno.nombre+ ', '+alumno.apellido,alumno.fecha_nac, alumno.rutina_id, alumno.entrenamiento_sistema, alumno.nivel_id]
         data.append(this_student)
         
     
     #table size
     width, height = A4
     table = Table(data, colWidths=[65 * mm, 30 * mm, 30 * mm, 35 * mm, 25 * mm])
     table.setStyle(TableStyle([
         ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
         ('BOX', (0,0), (-1,-1), 0.10, colors.black)]))
     table.wrapOn(c, width, height)
     table.drawOn(c, 30, high)
     c.showPage()
     
     c.save()
     
     pdf = buffer.getvalue()
     buffer.close()
     response.write(pdf)
     return response

     
    
def listadoAlumnos(request, pk):
    user = User.objects.get(id=pk)
    rutinas = list(Rutina.objects.filter(estado=True))
    print(rutinas)
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
            
        filtrado = 'Listado de alumnos filtrado por Rutinas, Tipo entrenamiento y Nivel'
            
        return render(request, 'rutina/listadoAlumnos.html', {'profesor' : profesor, 'mensaje' : mensaje, 'alumnos' : alumnos, 'rutinas':rutinas, 'filtrado':filtrado})
    
    if request.method == 'POST':
        rutinas = Rutina.objects.filter(estado=True)
        peticion = request.POST.copy()
        print(peticion)
        
        ruti = peticion.pop('rutinas')
        ruti = ruti[0]
    
        
        
        entrenamiento = peticion.pop('entrenamiento')
        entrenamiento = entrenamiento[0]
        
        nivel = peticion.pop('nivel')
        nivel = nivel[0]
        
        tipoPost = peticion.pop('tipoPost')
        tipoPost = tipoPost[0]
        
        
        if (Profesor.objects.filter(user_id=user.id).exists()):
            profesor = Profesor.objects.get(user_id=pk)
        else:
            return redirect('/home')
        
        filtrado = 'Listado de alumnos filtrado por ' + str(ruti)+', '+str(entrenamiento)+' y '+str(nivel)
        print(filtrado)
        alumnos = filtrar(ruti, entrenamiento, nivel, profesor)
        

        if (tipoPost == "filtro"):
            if (Alumno.objects.filter(profesor_id=profesor.id).exists()):
                mensaje = None
            else:
                mensaje = "Usted no tiene alumnos a cargo"
        else:
            if (Alumno.objects.filter(profesor_id=profesor.id).exists()):
                return reporte (request,alumnos)
                mensaje = None    
                            
            else:
                mensaje = "Usted no tiene alumnos a cargo"

        if (ruti != "Rutinas"):
            rutinas = Rutina.objects.exclude(nombre=ruti) 
            
        if entrenamiento != "Tipo entrenamiento":
            entrenamientoSeleccionado = entrenamiento
        else:
            entrenamientoSeleccionado = None
        
        if nivel != "Nivel":
            nivelSeleccionado = nivel
        else:
            nivelSeleccionado = None
                 
    return render(request, 'rutina/listadoAlumnos.html', {'profesor' : profesor, 'mensaje' : mensaje, 'alumnos' : alumnos, 'rutinas':rutinas, 'ruti':ruti, 'entrenamientoSeleccionado':entrenamientoSeleccionado, 'nivelSeleccionado':nivelSeleccionado,'filtrado':filtrado})         
        


"""class EliminarDisponibilidad(DeleteView):
    model = DisponibilidadProfesor
    def post(self,request, pk, *args, **kwargs):
        object = DisponibilidadProfesor.objects.get(id = pk)
        #Si un chico usa esa hora no se puede
        if (Rutina.objects.filter(actividad_id=object.id).exists()):
            mensaje = "Usted no puede borrar " + object.nombre + " porque ya pertenece a una rutina"
            return render(request, 'rutina/errorEliminacion.html',{'object':object, 'mensaje':mensaje})
        else:
            DisponibilidadProfesor.objects.get(id = object.id).delete()
        return redirect('/rutinas/actividades')"""   
    
    
      


"""def generar_pdf(request):
    print (request.POST)
    response = HttpResponse(content_type='application/pdf')
    pdf_name = "alumnos.pdf"  # llamado alumnos
    # la linea 26 es por si deseas descargar el pdf a tu computadora
    response['Content-Disposition'] = 'attachment; filename=filename=Listado.pdf'
    buff = BytesIO()
    doc = SimpleDocTemplate(buff,
                            pagesize=letter,
                            rightMargin=10,
                            leftMargin=25,
                            topMargin=60,
                            bottomMargin=18,
                            )
    listaAlumnos = []
    styles = getSampleStyleSheet()
    header = Paragraph("Listado de Alumnos", styles['Heading1'])
    listaAlumnos.append(header)
    headings = ('Nombre', 'Edad', 'Rutina', 'Nivel')
    allAlumnos = [(alumno.nombre, alumno.fecha_nac, alumno.rutina_id, alumno.nivel_id) for alumno in Alumno.objects.all()]
    print (allAlumnos)

    t = Table([headings] + allAlumnos)
    t.setStyle(TableStyle(
        [
            ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
            ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
            ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
        ]
    ))
    listaAlumnos.append(t)
    doc.build(listaAlumnos)
    response.write(buff.getvalue())
    buff.close()
    return response     

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
            error = form.error_messages
                
            return render(request, 'registro.html', context={'form': form, 'error':error})            

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
        form = DisponibilidadForm(request.POST)
        
        try:
            dias = peticion.pop('dias')
        except:
            mensaje = "No ha seleccionado los dias"
            return render(request, 'rutina/agregarDisponibilidad.html',{'form':form, 'mensaje':mensaje}) 
        
        try:
            inicio = peticion.pop('horario_inicio')
            hora_inicio = datetime.strptime(inicio[0], "%H:%M:%S").time()
               
            final = peticion.pop('horario_final')
            hora_final = datetime.strptime(final[0], "%H:%M:%S").time()
        except:
            mensaje = "Por favor ingrese correctamente el horario en el formato especificado (HH:MM:SS)"
            return render(request, 'rutina/agregarDisponibilidad.html',{'form':form,'mensaje':mensaje})
        
        
        #Controlamos que no exista esa disponibilidad
        for d in dias:
            print(d)
            if (DisponibilidadProfesor.objects.filter(semana_id=Semana.objects.get(dia=d).id, horario_inicio=hora_inicio, horario_final=hora_final).exists()):
                mensaje = "La disponibilidad ingresada ya existe."
                return render(request, 'rutina/agregarDisponibilidad.html',{'form':form, 'mensaje':mensaje})
        
        if form.is_valid():
            error = None
            if (hora_inicio<hora_final):
                i=0
                while i < len(dias):
                    semana = Semana.objects.get(dia=dias[i])
                    disponibilidad = DisponibilidadProfesor.objects.create(horario_inicio=hora_inicio, semana_id=semana, profesor_id=profesor, horario_final=hora_final)
                    disponibilidad.save()
                    i+=1
                mensaje = None
                disponibilidad = DisponibilidadProfesor.objects.filter(estado=True, profesor_id=profesor.id)
                messages.success(request, "Disponibilidad agregada con éxito.")
                sweetify.success(request, 'You successfully changed your password')
                return render(request, 'rutina/administrarDisponibilidad.html', {'disponibilidad':disponibilidad})
            else:
                mensaje = "El horario final no puede ser igual o menor al horario de inicio."
                return render(request, 'rutina/agregarDisponibilidad.html',{'form':form, 'dias':dias, 'mensaje':mensaje})
            
        else:
            error = form.errors
            mensaje = None
            return render(request, 'rutina/agregarDisponibilidad.html',{'form':form, 'dias':dias, 'mensaje':mensaje, 'error':error})
            
            
    else:
        form = DisponibilidadForm()
        mensaje = None
        return render(request, 'rutina/agregarDisponibilidad.html',{'form':form, 'dias':dias, 'mensaje':mensaje})
    
    return redirect ('/home/administracion/')