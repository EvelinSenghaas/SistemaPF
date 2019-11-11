from django import forms
from .models import Usuario, Profesor, Alumno, FichaAlumno, DisponibilidadProfesor
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
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
        widgets = {
            'username' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su nombre de usuario'}
                ),
            'email' : forms.EmailInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su correo electrónico'}
                ),
            'password1' : forms.PasswordInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su contraseña'}
                ),
            'password2' : forms.PasswordInput(
                attrs = { 'class':'form-control', 'placeholder': 'Repita su contraseña'}
                ),
            'first_name' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese sus nombres', 'required': True, 'pattern':'[A-Za-z ]+'}
                ),
            'last_name' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese sus apellidos', 'required': True, 'pattern':'[A-Za-z ]+'}
                ),
        }
    
        
        
        
    def save (self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
    
    

#Esto CREO que no se usa    
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
       super(LoginForm, self).__init__(*args, **kwargs)
       self.fields['username'].widget.attrs['class'] = 'form-control'
       self.fields['username'].widget.attrs['placeholder'] = 'Nombre de usuario'
       
       self.fields['password'].widget.attrs['class'] = 'form-control'
       self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
       
class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'apellido', 'fecha_nac', 'email']
        
        labels = {
            'nombre' : 'Nombre', 'apellido': 'Apellido', 'fecha_nac': 'Fecha de nacimiento', 'email': 'Correo electrónico',
            }
        widgets = {
            'nombre' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su nombre', 'readonly':'readonly'}
                ), 
            'apellido' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su apellido', 'readonly':'readonly'}
                ),
            'fecha_nac' : forms.DateTimeInput(
                attrs = { 'class':'form-control', 'placeholder': 'Fecha de nacimiento (dd/mm/aaaa)'}
                ),
            'email' : forms.EmailInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su correo electrónico', 'readonly':'readonly'}
                )
        }
        exclude = ('nombre', 'apellido', 'email')
        
        
        
        
class FichaForm(forms.ModelForm):
    class Meta:
        model = FichaAlumno
        fields = ['peso', 'sexo', 'altura', 'grupo_sanguineo', 'profesion']
        labels = {
            'peso' : 'Peso', 'sexo': 'Sexo', 'altura': 'Altura', 'grupo_sanguineo': 'Grupo sanguíneo', 'profesion': '¿A qué te dedicas?',
            }
        widgets = {
            'peso' : forms.NumberInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su peso (en kg)'}
                ), 
            'altura' : forms.NumberInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su altura (en metros)'}
                ),
            'profesion' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese su profesion'}
                )
        }
        
class DisponibilidadForm(forms.ModelForm):
    class Meta:
        model = DisponibilidadProfesor
        fields = ['horario_inicio', 'horario_final']
        labels = {
            'horario_inicio' : 'Horario de inicio',}
        widgets = {
            'horario_inicio' : forms.TimeInput(
                attrs = { 'class':'form-control', 'placeholder':'Formato (hh:mm:ss)'}
                ),
            'horario_final' : forms.TimeInput(
                attrs = { 'class':'form-control', 'placeholder':'Formato (hh:mm:ss)'}
                )}
    
    
        