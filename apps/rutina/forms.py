from django import forms
from .models import Detalle, Actividad, Rutina

class DetalleForm (forms.ModelForm):
    class Meta:
        model = Detalle
        fields = ['atributo', 'aspectoMejora']
    
class ActividadForm (forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['nombre', 'descripcion', 'detalle_id']
    
class RutinaForm (forms.ModelForm):
    class Meta:
        model = Rutina
        fields = ['nombre', 'descripcion', 'actividad_id']