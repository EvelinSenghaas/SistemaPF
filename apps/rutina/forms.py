from django import forms
from .models import Detalle, Actividad, Rutina

class DetalleForm (forms.ModelForm):
    class Meta:
        model = Detalle
        fields = ['categoria', 'musculo']
        labels = {
            'categoria' : 'Tren', 'musculo': 'Nombre del músculo',
        }
        widgets = {
            'categoria' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese el tren'}
                ), 'musculo' : forms.TextInput(
                    attrs = {
                        'class' : 'form-control', 'placeholder': 'Ingrese el musculo'
                    }
                )
        }
    
class ActividadForm (forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion', 'detalle_id']
        labels = {
            'nombre' : 'Nombre de la actividad', 'descripcion': 'Descripcion de la actividad', 'detalle_id': 'Detalles de la actividad', 'nivel_exigencia' : 'Nivel de exigencia'
        }
        widgets = {
            'nombre' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese el nombre de la actividad'}
                ), 'descripcion' : forms.Textarea(
                    attrs = {
                        'class' : 'form-control', 'placeholder': 'Ingrese la descripcion de la actividad'
                    }
                ), 'detalle_id' : forms.SelectMultiple(
                    attrs = {
                        'class' : 'form-control'
                    }
                )
        }
    
class RutinaForm (forms.ModelForm):
    class Meta:
        model = Rutina
        fields = [ 'nombre', 'descripcion', 'actividad_id']
        labels = {
            'nombre' : 'Nombre de la rutina', 'descripcion': 'Descripcion de la rutina', 'actividad_id': 'Actividades de la rutina',
        }
        widgets = {
            'nombre' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese el nombre de la rutina'}
                ), 'descripcion' : forms.Textarea(
                    attrs = {
                        'class' : 'form-control', 'placeholder': 'Ingrese la descripcion de la rutina'
                    }
                ), 'actividad_id' : forms.SelectMultiple(
                    attrs = {
                        'class' : 'form-control'
                    }
                )
        }
        