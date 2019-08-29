from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UsuarioForm
from .models import Usuario


# Create your views here.
def Home(request):
    return render(request,'home/home.html')

def registro(request):
    if request.method == 'POST':
        usuario = UsuarioForm(request.POST)
        if usuario.is_valid():
            usuario.save()
            return redirect('index')
        
    else:
        usuario = UsuarioForm()
        return render(request, 'registracion.html', {'usuario':usuario})