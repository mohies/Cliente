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
        self.fields["categoria"] = forms.ChoiceField(  # Cambiado de MultipleChoiceField a ChoiceField
            choices=categoriasDisponibles,
            required=True,
            help_text="Selecciona una categoría"
        )
        
class TorneoActualizarNombreForm(forms.Form):
    nombre = forms.CharField(
        label="Nuevo Nombre del Torneo",
        max_length=200,
        help_text="200 caracteres como máximo"
    )
    
    
class JuegoForm(forms.Form):
    GENEROS_CHOICES = [
        ("", "Selecciona un género"),  # Opción vacía por defecto
        ("Acción", "Acción"),
        ("Aventura", "Aventura"),
        ("Estrategia", "Estrategia"),
        ("Deportes", "Deportes"),
        ("RPG", "RPG"),
        ("Shooter", "Shooter"),
    ]

    nombre = forms.CharField(
        label="Nombre del Juego",
        required=True,
        max_length=200,
        help_text="200 caracteres como máximo"
    )
    
    descripcion = forms.CharField(
        label="Descripción",
        widget=forms.Textarea(),
        required=False,
        help_text="Mínimo 10 caracteres."
    )
    
    genero = forms.ChoiceField(
        label="Género",
        choices=GENEROS_CHOICES,
        required=False,  # 🔹 Permitir enviar vacío para que el servidor lo valide
        help_text="Selecciona un género"
    )

    def __init__(self, *args, **kwargs):
        super(JuegoForm, self).__init__(*args, **kwargs)
        
        helper = Helper()
        
        # Obtener los torneos disponibles desde la API
        torneosDisponibles = helper.obtener_torneos_select()
        self.fields["torneo"] = forms.ChoiceField(
            choices=torneosDisponibles,
            required=True,
            help_text="Selecciona un torneo"
        )
        
        # Obtener las consolas disponibles desde la API
        consolasDisponibles = helper.obtener_consolas_select()
        self.fields["id_consola"] = forms.ChoiceField(
            choices=consolasDisponibles,
            required=True,
            help_text="Selecciona una consola"
        )

class JuegoActualizarNombreForm(forms.Form):
    nombre = forms.CharField(
        label="Nuevo Nombre del Juego",
        max_length=200,
        help_text="200 caracteres como máximo"
    )
    
    
    
class ParticipanteForm(forms.Form):
    usuario = forms.ChoiceField(
        label="Usuario",
        required=False,
        help_text="Selecciona el usuario asociado",
    )

    puntos_obtenidos = forms.IntegerField(
    label="Puntos Obtenidos",
    required=False,
    help_text="Introduce los puntos obtenidos (pueden ser negativos o positivos)"
    )


    posicion_final = forms.IntegerField(
        label="Posición Final",
        required=False,
        help_text="Introduce la posición final (opcional)"
    )

    fecha_inscripcion = forms.DateField(
        label="Fecha de Inscripción",
        initial=datetime.date.today,
        widget=forms.SelectDateWidget(years=range(2000, 2030))
    )

    tiempo_jugado = forms.FloatField(
        label="Tiempo Jugado (horas)",
        required=False,
        min_value=0,
        help_text="Tiempo total jugado en horas"
    )

    def __init__(self, *args, **kwargs):
        super(ParticipanteForm, self).__init__(*args, **kwargs)
        
        helper = Helper()  # Instancia de Helper
        
        # Obtener los usuarios disponibles desde la API
        usuariosDisponibles = helper.obtener_usuarios_select()
        self.fields["usuario"].choices = usuariosDisponibles

        # Obtener los equipos disponibles desde la API
        equiposDisponibles = helper.obtener_equipos_select()
        self.fields["equipos"] = forms.MultipleChoiceField(
            choices=equiposDisponibles,
            required=False,  # Puede no tener equipos
            help_text="Mantén pulsada la tecla Control para seleccionar varios equipos"
        )


class ParticipanteActualizarEquiposForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ParticipanteActualizarEquiposForm, self).__init__(*args, **kwargs)

        helper = Helper()  # Instancia del Helper
        equiposDisponibles = helper.obtener_equipos_select()  # 🔹 Obtener equipos desde API

        self.fields["equipos"] = forms.MultipleChoiceField(
            choices=equiposDisponibles,
            required=False,  # ✅ Puede no tener equipos asignados
            help_text="Mantén pulsada la tecla Control para seleccionar varios equipos"
        )




class JugadorForm(forms.Form):
    usuario = forms.ChoiceField(
        label="Usuario",
        required=True,
        help_text="Selecciona el usuario que se convertirá en jugador"
    )
    
    puntos = forms.IntegerField(
        label="Puntos",
        required=False,
        min_value=0,
        help_text="Debe ser mayor o igual a 0"
    )
    
    equipo = forms.CharField(
        label="Equipo",
        required=False,
        max_length=100,
        help_text="Puedes dejarlo en blanco si el jugador no tiene equipo"
    )

    torneos = forms.MultipleChoiceField(
        label="Torneos",
        required=False,
        help_text="Mantén pulsado Ctrl para seleccionar varios torneos"
    )

    def __init__(self, *args, **kwargs):
        super(JugadorForm, self).__init__(*args, **kwargs)
        helper = Helper()
        
        # Obtener usuarios disponibles
        usuarios_disponibles = helper.obtener_usuarioslogin_select()
        self.fields["usuario"].choices = usuarios_disponibles
        
        # Obtener torneos disponibles
        torneos_disponibles = helper.obtener_torneos_select()
        self.fields["torneos"].choices = torneos_disponibles
        
        

class JugadorActualizarPuntosForm(forms.Form):
    puntos = forms.IntegerField(
        label="Actualizar Puntos",
        help_text="Introduce los puntos del jugador (debe ser un número positivo)"
    )













