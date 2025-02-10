from django import forms  # Importa el módulo de formularios
from django.forms import ModelForm  # Importa ModelForm directamente
from .models import *
from datetime import datetime, date, timedelta
from django.forms import DateInput
import datetime
from django.contrib.auth.forms import UserCreationForm
import json
from .helper import Helper

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




class TorneoForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre del Torneo",
        required=True, 
        max_length=200,
        help_text="200 caracteres como máximo"
    )
    
    descripcion = forms.CharField(
        label="Descripción",
        required=False,
        widget=forms.Textarea()
    )
    
    fecha_inicio = forms.DateField(
        label="Fecha de Inicio",
        initial=datetime.date.today,
        widget=forms.SelectDateWidget(years=range(1990, 2030))
    )
    
    duracion = forms.DurationField(label="Duración")

    def __init__(self, *args, **kwargs):
        super(TorneoForm, self).__init__(*args, **kwargs)
        
        helper = Helper()
        
        # Obtener los participantes disponibles desde la API
        participantesDisponibles = helper.obtener_participantes_select()
        self.fields["participantes"] = forms.MultipleChoiceField(
            choices=participantesDisponibles,
            required=True,
            help_text="Mantén pulsada la tecla Control para seleccionar varios elementos"
        )
        
        # Obtener las categorías disponibles desde la API
        categoriasDisponibles = helper.obtener_categorias_select()
        self.fields["categoria"] = forms.ChoiceField(  # 🔹 Cambiado de MultipleChoiceField a ChoiceField
            choices=categoriasDisponibles,
            required=True,
            help_text="Selecciona una categoría"
        )



















