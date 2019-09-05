from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from .forms import NewUserForm, UsuarioForm
from django.views.generic import TemplateView


# Create your views here.
class Home(TemplateView):
    template_name = "home/home.html"


def registro(request):               
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            dj_login(request, user)
            return redirect ('/home/cargar_datos')
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


def cargarDatosUsuario(request):
    if request.method == 'POST':
        userForm = UsuarioForm(request.POST)
        if userForm.is_valid():
            userForm.save()
            return redirect ('/home')
    else:
        userForm = UsuarioForm()
        return render(request, 'cargarDatos.html', {'userForm':userForm})