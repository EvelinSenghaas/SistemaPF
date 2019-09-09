from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, UsuarioForm, LoginForm
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


# Create your views here.
class Home(TemplateView):
    template_name = "home/home.html"
    
class Administrar(PermissionRequiredMixin,TemplateView):
    permission_required = 'rutina.change_rutina'
    template_name = "home/administracion.html"
    
class PaginaInicial(TemplateView):
    template_name = "home/paginaInicial.html"


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