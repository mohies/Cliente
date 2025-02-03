from django.shortcuts import render,redirect
from .forms import *
import requests
import environ
import os

# Inicializa environ.Env
env = environ.Env()

# Construye el path de BASE_DIR (en settings.py ya está definido, pero si no, agrégalo)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carga las variables del archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

USER_KEY_ADMINISTRADOR = env("USER_KEY_ADMINISTRADOR")
USER_KEY_JUGADOR = env("USER_KEY_JUGADOR")
USER_KEY_ORGANIZADOR = env("USER_KEY_ORGANIZADOR")
print(USER_KEY_ADMINISTRADOR)
# Create your views here.


def crear_cabecera():
    return {
        'Authorization': 'Bearer X0UrP3LbSeYnv43TQwdGcAfz96LprV'
        }
def index(request):
    return render(request, 'index.html')


def torneos_lista_api(request):
    # Obtenemos todos los torneos desde la API
    headers = {'Authorization': f'Bearer {USER_KEY_ADMINISTRADOR}'}
    response = requests.get('http://127.0.0.1:8000/api/v1/torneos/mejorada/', headers=headers)  # Cambia la URL si es necesario
    
    # Transformamos la respuesta en JSON
    torneos = response.json()
    
    # Renderizamos los datos en la plantilla HTML
    return render(request, 'cliente/lista_api.html', {"torneos_mostrar": torneos})


def participantes_lista_api(request):
    # Obtenemos todos los participantes desde la API
    headers = {'Authorization': f'Bearer {USER_KEY_JUGADOR}'}
    response = requests.get('https://mohbenbou.pythonanywhere.com/api/v1/participantes/mejorada/', headers=headers)  # Cambia la URL si es necesario
    
    # Transformamos la respuesta en JSON
    participantes = response.json()
    
    # Renderizamos los datos en la plantilla HTML
    return render(request, 'cliente/lista_participantes.html', {"participantes_mostrar": participantes})



def juegos_lista_api(request):
    # Obtenemos todos los juegos desde la API
    headers = {'Authorization': f'Bearer {USER_KEY_ORGANIZADOR}'}
    response = requests.get('https://mohbenbou.pythonanywhere.com/api/v1/juegos/mejorada/', headers=headers)  # Cambia la URL si es necesario
    
    # Transformamos la respuesta en JSON
    juegos = response.json()
    
    # Renderizamos los datos en la plantilla HTML
    return render(request, 'cliente/lista_juegos.html', {"juegos_mostrar": juegos})






def equipos_lista_api(request):
    # El token que te han dado
    access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4MTk4Nzc3LCJpYXQiOjE3MzgxOTg0NzcsImp0aSI6ImNmM2ZiMjcwOWYxNDRiNTg4NjAwYTcxYjA0NWZmZWQ3IiwidXNlcl9pZCI6Mn0.-gGn8ViwXz6rhXkchXiJJ4j3mqFNwJwMvJyvqhUIqpY'
    
    # Usamos el access token para hacer una solicitud a la API de equipos
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://mohbenbou.pythonanywhere.com/api/v1/equipos/', headers=headers)

    # Si la respuesta es exitosa, mostramos los equipos
    if response.status_code == 200:
        equipos = response.json()
        return render(request, 'cliente/lista_equipos.html', {"equipos_mostrar": equipos})


def torneo_busqueda_simple(request):
    formulario = BusquedaTorneoForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera() 
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/torneos/buscar',
            headers=headers,
            params={'textoBusqueda': formulario.data.get("textoBusqueda")}
        )
        torneos = response.json()
        return render(request, 'cliente/lista_api.html', {"torneos_mostrar": torneos})
    
    if "HTTP_REFERER" in request.META:
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    
    
def torneo_busqueda_avanzada(request):
    formulario = BusquedaAvanzadaTorneoForm(request.GET or None)
    
    if request.GET:  # Verifica si hay datos en la solicitud GET. Esto significa que el formulario ha sido enviado con datos.
        headers = crear_cabecera()
        params = {
            'textoBusqueda': request.GET.get('textoBusqueda', ''),
            'fecha_desde': request.GET.get('fecha_desde', None),
            'fecha_hasta': request.GET.get('fecha_hasta', None),
        }
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/torneos/buscar/avanzado',
            headers=headers,
            params=params
        )
        torneos = response.json()
        return render(request, 'cliente/lista_api.html', {"torneos_mostrar": torneos})
    
    return render(request, 'cliente/busqueda_avanzada.html', {"formulario": formulario})


def equipo_busqueda_avanzada(request):
    formulario = BusquedaAvanzadaEquipoForm(request.GET or None)
    
    if request.GET:
        headers = crear_cabecera()
        params = {
            'nombre': request.GET.get('nombre', ''),
            'fecha_ingreso_desde': request.GET.get('fecha_ingreso_desde', ''),
            'fecha_ingreso_hasta': request.GET.get('fecha_ingreso_hasta', ''),
            'puntos_contribuidos_min': request.GET.get('puntos_contribuidos_min', ''),
        }
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/equipos/buscar/avanzado',
            headers=headers,
            params=params
        )
        equipos = response.json()
        return render(request, 'cliente/lista_equipos.html', {"equipos_mostrar": equipos})
    
    return render(request, 'cliente/busqueda_avanzada_equipo.html', {"formulario": formulario})


def participante_busqueda_avanzada(request):
    formulario = BusquedaAvanzadaParticipanteForm(request.GET or None)
    
    if request.GET:
        headers = crear_cabecera()
        params = {
            'nombre': request.GET.get('nombre', ''),
            'puntos_obtenidos_min': request.GET.get('puntos_obtenidos_min', ''),
            'fecha_inscripcion_desde': request.GET.get('fecha_inscripcion_desde', ''),
            'fecha_inscripcion_hasta': request.GET.get('fecha_inscripcion_hasta', ''),
        }
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/participantes/buscar/avanzado',
            headers=headers,
            params=params
        )
        participantes = response.json()
        return render(request, 'cliente/lista_participantes.html', {"participantes_mostrar": participantes})
    
    return render(request, 'cliente/busqueda_avanzada_participante.html', {"formulario": formulario})


def juego_busqueda_avanzada(request):
    formulario = BusquedaAvanzadaJuegoForm(request.GET or None)
    
    if request.GET:
        headers = crear_cabecera()
        params = {
            'nombre': request.GET.get('nombre', ''),
            'genero': request.GET.get('genero', ''),
            'fecha_participacion_desde': request.GET.get('fecha_participacion_desde', ''),
            'fecha_participacion_hasta': request.GET.get('fecha_participacion_hasta', ''),
        }
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/juegos/buscar/avanzado',
            headers=headers,
            params=params
        )
        juegos = response.json()
        return render(request, 'cliente/lista_juegos.html', {"juegos_mostrar": juegos})
    
    return render(request, 'cliente/busqueda_avanzada_juego.html', {"formulario": formulario})
