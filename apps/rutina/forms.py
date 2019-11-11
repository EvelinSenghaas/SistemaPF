from django import forms
from .models import Detalle, Actividad, Rutina, Nivel, Repeticion, EvaluacionNivel

class DetalleForm (forms.ModelForm):
    class Meta:
        model = Detalle
        fields = ['categoria', 'musculo']
        labels = {
            'categoria' : 'Tren', 'musculo': 'Nombre del músculo',
        }
        widgets = {
            'categoria' : forms.TextInput(
                attrs = { 'class':'form-control', 'placeholder': 'Ingrese el tren', 'pattern':'[A-Za-z ]+'}
                ), 'musculo' : forms.TextInput(
                    attrs = {
                        'class' : 'form-control', 'placeholder': 'Ingrese el musculo', 'pattern':'[A-Za-z ]+'
                    }
                )
        }
    
class ActividadForm (forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion','detalle_id']
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
        
class NivelForm (forms.ModelForm):
    class Meta:
        model = Nivel
        fields = ['nombre']
        widgets = {
            'nombre' : forms.Select(
                attrs = { 'class':'form-control'}
                )
        }
        
class RepeticionForm (forms.ModelForm):
    class Meta:
        model = Repeticion
        fields = ['repeticionesMinimas', 'nivel_id']
        widgets = {
            'repeticionesMinimas' : forms.NumberInput(
                attrs = { 'class':'form-control col-2 ', 'style':'margin-left:4%', 'placeholder':'Repeticiones'}
                ), 'nivel_id' : forms.Select(
                attrs = { 'class':'custom-select col-3', 'style':'margin-left:2%',}
                ),
        }
        
class EvaluacionNivelForm(forms.ModelForm):
    class Meta:
        model = EvaluacionNivel
        fields = ['nivel_id', 'cantSesiones']
        widgets = {
            'cantSesiones' : forms.NumberInput(
                attrs = { 'class':'form-control'}
                ), 'nivel_id' : forms.Select(
                attrs = { 'class':'form-class'}
                ),
        }