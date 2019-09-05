from django.shortcuts import render, redirect
from .models import Rutina, Actividad, Detalle
from .forms import DetalleForm, ActividadForm, RutinaForm
from django.views.generic import View, TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.
    
class Rutinas (TemplateView):
    def get(self, request, *args, **kwargs):
        return render(request, 'rutina/rutinas.html')

    

#Listados
class ListadoRutinas (PermissionRequiredMixin,ListView):
    permission_required = ('rutina.view_rutina','rutina.add_rutina','rutina.edit_rutina','rutina.delete_rutina')
    template_name = 'rutina/rutinas.html'
    context_object_name = 'rutinas'
    queryset = Rutina.objects.filter(estado=True)

class ListadoActividades (PermissionRequiredMixin,ListView):
    permission_required = ('actividad.view_actividad','actividad.add_actividad','actividad.edit_actividad','actividad.delete_actividad')
    template_name = 'rutina/actividades.html'
    context_object_name = 'actividades'
    queryset = Actividad.objects.filter(estado=True)    
    
    
def verRutina(request, pk):
    rutina = Rutina.objects.get(id = pk)
    return render (request, 'rutina/verRutina.html', { 'rutina': rutina})
       

#Agregar    
class AgregarDetalle(PermissionRequiredMixin, CreateView):
    permission_required = 'detalle.add_detalle'
    model = Detalle
    form_class = DetalleForm
    template_name = 'rutina/agregarDetalle.html'
    succes_name = reverse_lazy('/rutinas')
    
class AgregarActividad(PermissionRequiredMixin, CreateView):
    permission_required = 'actividad.add_actividad'
    model = Actividad
    template_name = 'rutina/agregarActividad.html'
    form_class = ActividadForm
    succes_name = reverse_lazy('/rutinas')

    
class AgregarRutina(PermissionRequiredMixin, CreateView):
    permission_required = 'rutina.add_rutina'
    model = Rutina
    form_class = RutinaForm
    template_name = 'rutina/agregarRutina.html'
    succes_name = reverse_lazy('/rutinas')
 
#Editar    
class EditarRutina(PermissionRequiredMixin,UpdateView):
    permission_required = 'rutina.edit_rutina'
    model = Rutina
    template_name = 'rutina/agregarRutina.html'
    form_class = RutinaForm
    succes_url = reverse_lazy('/rutinas')
    

class EditarActividad(PermissionRequiredMixin,UpdateView):
    permission_required = 'actividad.edit_actividad'
    model = Actividad
    template_name = 'rutina/agregarActividad.html'
    form_class = ActividadForm
    succes_url = reverse_lazy('/rutinas')
    
class EditarDetalle(PermissionRequiredMixin,UpdateView):
    permission_required = 'detalle.edit_detalle'
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
    
class EliminarActividad(DeleteView):
    model = Actividad
    def post(self,request, pk, *args, **kwargs):
        object = Actividad.objects.get(id = pk)
        object.estado = False
        object.save()
        return redirect('/rutinas/actividades')
