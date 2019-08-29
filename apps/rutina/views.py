from django.shortcuts import render, redirect
from .models import Rutina
from .forms import DetalleForm, ActividadForm, RutinaForm

# Create your views here.


"""def listarAutores(request):
    autores = Autor.objects.all()
    return render(request, 'libro/listar_autor.html', {'autores':autores})"""
    
def Rutinas(request):
    return render(request, 'rutina/rutinas.html')

def listarRutinas(request):
    rutinas = Rutina.objects.all()
    print(rutinas)
    return render(request, 'rutina/rutinas.html', {'rutinas':rutinas})


def agregarDetalle(request):
    if request.method == 'POST':
        detalleForm = DetalleForm(request.POST)
        if detalleForm.is_valid():
            detalleForm.save()
            return redirect ('/rutinas')
    else:
        detalleForm = DetalleForm()
        return render(request, 'rutina/agregarDetalle.html',{'detalleForm':detalleForm})


def agregarActividad(request):
    if request.method == 'POST':
        actividadForm = ActividadForm(request.POST)
        if actividadForm.is_valid():
            actividadForm.save()
            return redirect ('/rutinas')
    else:
        actividadForm = ActividadForm()
        return render(request, 'rutina/agregarActividad.html',{'actividadForm':actividadForm})
    
def agregarRutina(request):
    if request.method == 'POST':
        rutinaForm = RutinaForm(request.POST)
        if rutinaForm.is_valid():
            rutinaForm.save()
            return redirect ('/rutinas')
    else:
        rutinaForm = RutinaForm()
        return render(request, 'rutina/agregarRutina.html',{'rutinaForm':rutinaForm})