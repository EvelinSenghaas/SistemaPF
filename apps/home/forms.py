from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario #este atributo hace referencia al modelo al que pertenece
        fields = ['nombreUsuario', 'contrasena', 'correo', 'nombres', 'apellidos', 'fechaNac', 'sexo', 'nacionalidad', 'altura', 'peso'] #campos del modelo a ser rellenado