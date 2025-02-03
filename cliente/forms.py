from django import forms  # Importa el módulo de formularios
from django.forms import ModelForm  # Importa ModelForm directamente
from .models import *
from datetime import datetime, date, timedelta
from django.forms import DateInput
import datetime
from django.contrib.auth.forms import UserCreationForm

class BusquedaTorneoForm(forms.Form):
    textoBusqueda = forms.CharField(required=True)
    
    
class BusquedaAvanzadaTorneoForm(forms.Form):
    textoBusqueda = forms.CharField(required=False)
    
    categorias = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Introduce las categorías separadas por comas'})
    )

    fecha_desde = forms.DateField(label="Fecha Desde", 
                                  required=False, 
                                  widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}))

    fecha_hasta = forms.DateField(label="Fecha Hasta", 
                                  required=False,
                                  widget=forms.DateInput(format="%Y-%m-%d", 
                                                         attrs={"type": "date", "class": "form-control"}))

    # Filtrar por duración mínima de los torneos
    duracion_minima = forms.TimeField(label="Duración mínima", 
                                      required=False, 
                                      widget=forms.TimeInput(attrs={"type": "time", "class": "form-control"}))
    

class BusquedaAvanzadaEquipoForm(forms.Form):
    nombre = forms.CharField(required=False)
    fecha_ingreso_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    fecha_ingreso_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    puntos_contribuidos_min = forms.IntegerField(required=False)

class BusquedaAvanzadaParticipanteForm(forms.Form):
    nombre = forms.CharField(required=False)
    puntos_obtenidos_min = forms.IntegerField(required=False)
    fecha_inscripcion_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    fecha_inscripcion_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))

class BusquedaAvanzadaJuegoForm(forms.Form):
    nombre = forms.CharField(required=False)
    genero = forms.CharField(required=False)
    fecha_participacion_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    fecha_participacion_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))


class RegistroForm(UserCreationForm):
    roles = (
        ('Jugador'),
        ( 'Organizador'),
    )

    rol = forms.ChoiceField(choices=roles, label="Rol", required=True)

    class Meta:
        fields = ('username', 'email', 'password1', 'password2', 'rol')


class RegistroJugadorForm(forms.ModelForm):
    class Meta:
        fields = ['puntos', 'equipo']


class RegistroOrganizadorForm(forms.ModelForm):
    class Meta:
        fields = ['eventos_creados']








        




    



   
