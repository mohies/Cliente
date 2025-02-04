from django.shortcuts import render,redirect
from .forms import *
import requests
import environ
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import xml.etree.ElementTree as ET

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
        'Authorization': 'Bearer rYAaupTkN4FCfHZ4qS7tYXOrscolMZ'
        }

# Definimos por defecto la version que tenemos de la API y las establecemos en nuestras aplicaciones
API_VERSION = env("API_VERSION", default="v1") 
API_BASE_URL = f'http://127.0.0.1:8000/api/{API_VERSION}/'
print(API_BASE_URL)

def index(request):
    return render(request, 'index.html')

def process_response(response):
    # Verifica si el tipo de contenido es 'application/json'
    if response.headers['Content-Type'] == 'application/json':
        # Si es JSON, convierte el contenido de la respuesta a un objeto Python (como un diccionario o lista)
        return response.json()
    
    # Verifica si el tipo de contenido es 'application/xml'
    elif response.headers['Content-Type'] == 'application/xml':
        # Si es XML, convierte el contenido de la respuesta en un árbol de elementos XML usando ElementTree
        return ET.fromstring(response.content)
    
    # Si el tipo de contenido no es ni JSON ni XML, lanza un error
    else:
        raise ValueError('Unsupported content type: {}'.format(response.headers['Content-Type']))


def torneos_lista_api(request):
    # Obtenemos todos los torneos desde la API
    headers = {'Authorization': f'Bearer {USER_KEY_ADMINISTRADOR}'}
    response = requests.get(f'{API_BASE_URL}torneos/mejorada/', headers=headers)  # Cambia la URL si es necesario
    
    # Procesamos la respuesta
    torneos = process_response(response)
    
    # Renderizamos los datos en la plantilla HTML
    return render(request, 'cliente/lista_api.html', {"torneos_mostrar": torneos})


def participantes_lista_api(request):
    # Obtenemos todos los participantes desde la API
    headers = {'Authorization': f'Bearer {USER_KEY_JUGADOR}'}
    response = requests.get(f'{API_BASE_URL}participantes/mejorada/', headers=headers)  # Cambia la URL si es necesario
    
    # Procesamos la respuesta
    participantes = process_response(response)
    
    # Renderizamos los datos en la plantilla HTML
    return render(request, 'cliente/lista_participantes.html', {"participantes_mostrar": participantes})



def juegos_lista_api(request):
    # Obtenemos todos los juegos desde la API
    headers = {'Authorization': f'Bearer {USER_KEY_ORGANIZADOR}'}
    response = requests.get(f'{API_BASE_URL}juegos/mejorada/', headers=headers)  # Cambia la URL si es necesario
    
    # Procesamos la respuesta
    juegos = process_response(response)
    
    # Renderizamos los datos en la plantilla HTML
    return render(request, 'cliente/lista_juegos.html', {"juegos_mostrar": juegos})






def equipos_lista_api(request):
    # El token que te han dado
    access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4MTk4Nzc3LCJpYXQiOjE3MzgxOTg0NzcsImp0aSI6ImNmM2ZiMjcwOWYxNDRiNTg4NjAwYTcxYjA0NWZmZWQ3IiwidXNlcl9pZCI6Mn0.-gGn8ViwXz6rhXkchXiJJ4j3mqFNwJwMvJyvqhUIqpY'
    
    # Usamos el access token para hacer una solicitud a la API de equipos
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{API_BASE_URL}equipos/', headers=headers)

    # Procesamos la respuesta
    if response.status_code == 200:
        equipos = process_response(response)
        return render(request, 'cliente/lista_equipos.html', {"equipos_mostrar": equipos})


def torneo_busqueda_simple(request):
    formulario = BusquedaTorneoForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera() 
        response = requests.get(
            f'{API_BASE_URL}torneos/buscar',
            headers=headers,
            params={'textoBusqueda': formulario.data.get("textoBusqueda")}
        )
        torneos = process_response(response)
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
            f'{API_BASE_URL}torneos/buscar/avanzado',
            headers=headers,
            params=params
        )
        torneos = process_response(response)
        return render(request, 'cliente/lista_api.html', {"torneos_mostrar": torneos})
    
    return render(request, 'cliente/busqueda_avanzada.html', {"formulario": formulario})


@api_view(['GET'])
def equipo_busqueda_avanzada(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaEquipoForm(request.GET)
        if formulario.is_valid():
            try:
                headers = crear_cabecera()
                response = requests.get(
                    f'{API_BASE_URL}equipos/buscar/avanzado',
                    headers=headers,
                    params=formulario.cleaned_data
                )
                if response.status_code == requests.codes.ok:
                    equipos = process_response(response)
                    return render(request, 'cliente/lista_equipos.html', {"equipos_mostrar": equipos})
                else:
                    response.raise_for_status()
            except requests.HTTPError as http_err:
                print(f'Hubo un error en la petición: {http_err}')
                if response.status_code == 400:
                    errores = process_response(response)
                    for campo, mensaje in errores.items():
                        formulario.add_error(campo, mensaje)
                    return render(request, 'cliente/busqueda_avanzada_equipo.html', {"formulario": formulario, "errores": errores})
                else:
                    return tratar_errores(request, response.status_code)
            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return tratar_errores(request, 500)
        else:
            return render(request, 'cliente/busqueda_avanzada_equipo.html', {"formulario": formulario})
    else:
        formulario = BusquedaAvanzadaEquipoForm(None)
    return render(request, 'cliente/busqueda_avanzada_equipo.html', {"formulario": formulario})

@api_view(['GET'])
def participante_busqueda_avanzada(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaParticipanteForm(request.GET)
        try:
            headers = crear_cabecera()
            response = requests.get(
                f'{API_BASE_URL}participantes/buscar/avanzado',
                headers=headers,
                params=formulario.data
            )
            if response.status_code == requests.codes.ok:
                participantes = process_response(response)
                return render(request, 'cliente/lista_participantes.html', {"participantes_mostrar": participantes})
            else:
                print(response.status_code)
                response.raise_for_status()
        except requests.HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:
                errores = process_response(response)
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'cliente/busqueda_avanzada_participante.html', {"formulario": formulario, "errores": errores})
            else:
                return tratar_errores(request, response.status_code)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return tratar_errores(request, 500)
    else:
        formulario = BusquedaAvanzadaParticipanteForm(None)
    return render(request, 'cliente/busqueda_avanzada_participante.html', {"formulario": formulario})

@api_view(['GET'])
def juego_busqueda_avanzada(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaJuegoForm(request.GET)
        try:
            headers = crear_cabecera()
            response = requests.get(
                f'{API_BASE_URL}juegos/buscar/avanzado',
                headers=headers,
                params=formulario.data
            )
            if response.status_code == requests.codes.ok:
                juegos = process_response(response)
                return render(request, 'cliente/lista_juegos.html', {"juegos_mostrar": juegos})
            else:
                print(response.status_code)
                response.raise_for_status()
        except requests.HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:
                errores = process_response(response)
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'cliente/busqueda_avanzada_juego.html', {"formulario": formulario, "errores": errores})
            else:
                return tratar_errores(request, response.status_code)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return tratar_errores(request, 500)
    else:
        formulario = BusquedaAvanzadaJuegoForm(None)
    return render(request, 'cliente/busqueda_avanzada_juego.html', {"formulario": formulario})




def tratar_errores(request,codigo):
    if codigo == 404:
        return mi_error_404(request)
    else:
        return mi_error_500(request)
        


#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'cliente/errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'cliente/errores/500.html',None,None,500)