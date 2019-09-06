from django import forms
from .models import Usuario
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Permission

class UsuarioForm():
    class Meta:
        model = Usuario
        fields = ['username', 'password', 'email', 'nombres', 'apellidos', 'fechaNac', 'sexo', 'nacionalidad', 'altura', 'peso']
    
            
class NewUserForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','first_name', 'last_name']
        labels = {
            'username' : 'Nombre de usuario', 'email': 'Correo electronico', 'password1': 'Contraseña', 'password2': 'Repetir contraseña', 'first_name': 'Nombres', 'last_name': 'Apellidos',
        }
    
    def save (self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()

        return user