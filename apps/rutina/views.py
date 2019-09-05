from django.shortcuts import render, redirect
from .models import Rutina, Actividad, Detalle
from .forms import DetalleForm, ActividadForm, RutinaForm
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy

# Create your views here.
    
class Rutinas (TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'rutina/rutinas.html')
    
#Listados
class ListadoRutinas (ListView):
    template_name = 'rutina/rutinas.html'
    context_object_name = 'rutinas'
    queryset = Rutina.objects.filter(estado=True)
    
    
    
def verRutina(request, pk):
    rutina = Rutina.objects.get(id = pk)
    return render (request, 'rutina/verRutina.html', { 'rutina': rutina})
       

#Agregar    
class AgregarDetalle(CreateView):
    model = Detalle
    form_class = DetalleForm
    template_name = 'rutina/agregarDetalle.html'
    succes_name = reverse_lazy('/rutinas')
    
class AgregarActividad(CreateView):
    model = Actividad
    template_name = 'rutina/agregarActividad.html'
    form_class = ActividadForm
    succes_name = reverse_lazy('/rutinas')
    
class AgregarRutina(CreateView):
    model = Rutina
    form_class = RutinaForm
    template_name = 'rutina/agregarRutina.html'
    succes_name = reverse_lazy('/rutinas')
 
#Editar    
class EditarRutina(UpdateView):
    model = Rutina
    template_name = 'rutina/agregarRutina.html'
    form_class = RutinaForm
    succes_url = reverse_lazy('/rutinas')
    

class EditarActividad(UpdateView):
    model = Actividad
    template_name = 'rutina/agregarActividad.html'
    form_class = ActividadForm
    succes_url = reverse_lazy('/rutinas')
    
class EditarDetalle(UpdateView):
    model = Detalle
    template_name = 'rutina/agregarDetalle.html'
    form_class = DetalleForm
    succes_url = reverse_lazy('/rutinas')
    
#Eliminar
class EliminarRutina(DeleteView):
    model = Rutina
    def post(self,request, pk, *args, **kwargs):
        object = Rutina.objects.get(id = pk)
        object.estado = False
        object.save()
        return redirect('/rutinas')
