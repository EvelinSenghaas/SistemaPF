from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as dj_login, logout, authenticate
from django.contrib import messages
from .forms import UsuarioForm
from .models import Usuario


# Create your views here.
def Home(request):
    return render(request,'home/home.html')

#def registro(request):
    

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