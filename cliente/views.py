from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *
import requests
import environ
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import xml.etree.ElementTree as ET
from requests.exceptions import HTTPError
import json
import logging

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

# Configurar el logger
logger = logging.getLogger(__name__)

def crear_cabecera():
    return {
        'Authorization': 'Bearer PUHJyMz5miDrM6vYCQK6gd7LQxeuMf',
        "Content-Type": "application/json"
        }

# Definimos por defecto la version que tenemos de la API y las establecemos en nuestras aplicaciones
API_VERSION = env("API_VERSION", default="v1") 
API_BASE_URL = f'http://127.0.0.1:8000/api/{API_VERSION}/'

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
    try:
        headers = {'Authorization': f'Bearer {USER_KEY_ADMINISTRADOR}'}
        response = requests.get(f'{API_BASE_URL}torneos/mejorada/', headers=headers)
        torneos = process_response(response)
        return render(request, 'cliente/lista_api.html', {"torneos_mostrar": torneos})
    except Exception as err:
        logger.error(f'Error al obtener la lista de torneos: {err}')
        return mi_error_500(request)

def participantes_lista_api(request):
    try:
        headers = {'Authorization': f'Bearer {USER_KEY_JUGADOR}'}
        response = requests.get(f'{API_BASE_URL}participantes/mejorada/', headers=headers)
        participantes = process_response(response)
        return render(request, 'cliente/lista_participantes.html', {"participantes_mostrar": participantes})
    except Exception as err:
        logger.error(f'Error al obtener la lista de participantes: {err}')
        return mi_error_500(request)

def juegos_lista_api(request):
    try:
        headers = {'Authorization': f'Bearer {USER_KEY_ORGANIZADOR}'}
        response = requests.get(f'{API_BASE_URL}juegos/mejorada/', headers=headers)
        juegos = process_response(response)
        return render(request, 'cliente/lista_juegos.html', {"juegos_mostrar": juegos})
    except Exception as err:
        logger.error(f'Error al obtener la lista de juegos: {err}')
        return mi_error_500(request)

def equipos_lista_api(request):
    try:
        access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4MTk4Nzc3LCJpYXQiOjE3MzgxOTg0NzcsImp0aSI6ImNmM2ZiMjcwOWYxNDRiNTg4NjAwYTcxYjA0NWZmZWQ3IiwidXNlcl9pZCI6Mn0.-gGn8ViwXz6rhXkchXiJJ4j3mqFNwJwMvJyvqhUIqpY'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(f'{API_BASE_URL}equipos/', headers=headers)
        if response.status_code == 200:
            equipos = process_response(response)
            return render(request, 'cliente/lista_equipos.html', {"equipos_mostrar": equipos})
        else:
            response.raise_for_status()
    except Exception as err:
        logger.error(f'Error al obtener la lista de equipos: {err}')
        return mi_error_500(request)

def torneo_busqueda_simple(request):
    try:
        formulario = BusquedaTorneoForm(request.GET)
        if formulario.is_valid():
            headers = crear_cabecera()
            response = requests.get(
                f'{API_BASE_URL}torneos/buscar/',
                headers=headers,
                params={'textoBusqueda': formulario.data.get("textoBusqueda")}
            )
            torneos = process_response(response)
            return render(request, 'cliente/lista_api.html', {"torneos_mostrar": torneos})
        if "HTTP_REFERER" in request.META:
            return redirect(request.META["HTTP_REFERER"])
        else:
            return redirect("index")
    except Exception as err:
        logger.error(f'Error en la búsqueda simple de torneos: {err}')
        return mi_error_500(request)

def torneo_busqueda_avanzada(request):
    try:
        formulario = BusquedaAvanzadaTorneoForm(request.GET)
        if request.GET:
            headers = crear_cabecera()
            params = {
                'textoBusqueda': request.GET.get('textoBusqueda', ''),
                'fecha_desde': request.GET.get('fecha_desde', None),
                'fecha_hasta': request.GET.get('fecha_hasta', None),
            }
            response = requests.get(
                f'{API_BASE_URL}torneos/buscar/avanzado/',
                headers=headers,
                params=params
            )
            torneos = process_response(response)
            return render(request, 'cliente/lista_api.html', {"torneos_mostrar": torneos})
        return render(request, 'cliente/busqueda_avanzada.html', {"formulario": formulario})
    except Exception as err:
        logger.error(f'Error en la búsqueda avanzada de torneos: {err}')
        return mi_error_500(request)

@api_view(['GET'])
def equipo_busqueda_avanzada(request):
    try:
        if len(request.GET) > 0:
            formulario = BusquedaAvanzadaEquipoForm(request.GET)
            if formulario.is_valid():
                headers = crear_cabecera()
                response = requests.get(
                    f'{API_BASE_URL}equipos/buscar/avanzado/',
                    headers=headers,
                    params=formulario.cleaned_data
                )
                if response.status_code == requests.codes.ok:
                    equipos = process_response(response)
                    return render(request, 'cliente/lista_equipos.html', {"equipos_mostrar": equipos})
                else:
                    response.raise_for_status()
            else:
                return render(request, 'cliente/busqueda_avanzada_equipo.html', {"formulario": formulario})
        else:
            formulario = BusquedaAvanzadaEquipoForm(None)
        return render(request, 'cliente/busqueda_avanzada_equipo.html', {"formulario": formulario})
    except Exception as err:
        logger.error(f'Error en la búsqueda avanzada de equipos: {err}')
        return mi_error_500(request)

@api_view(['GET'])
def participante_busqueda_avanzada(request):
    try:
        if len(request.GET) > 0:
            formulario = BusquedaAvanzadaParticipanteForm(request.GET)
            headers = crear_cabecera()
            response = requests.get(
                f'{API_BASE_URL}participantes/buscar/avanzado/',
                headers=headers,
                params=formulario.data
            )
            if response.status_code == requests.codes.ok:
                participantes = process_response(response)
                return render(request, 'cliente/lista_participantes.html', {"participantes_mostrar": participantes})
            else:
                response.raise_for_status()
        else:
            formulario = BusquedaAvanzadaParticipanteForm(None)
        return render(request, 'cliente/busqueda_avanzada_participante.html', {"formulario": formulario})
    except Exception as err:
        logger.error(f'Error en la búsqueda avanzada de participantes: {err}')
        return mi_error_500(request)

@api_view(['GET'])
def juego_busqueda_avanzada(request):
    try:
        if len(request.GET) > 0:
            formulario = BusquedaAvanzadaJuegoForm(request.GET)
            headers = crear_cabecera()
            response = requests.get(
                f'{API_BASE_URL}juegos/buscar/avanzado/',
                headers=headers,
                params=formulario.data
            )
            if response.status_code == requests.codes.ok:
                juegos = process_response(response)
                return render(request, 'cliente/lista_juegos.html', {"juegos_mostrar": juegos})
            else:
                response.raise_for_status()
        else:
            formulario = BusquedaAvanzadaJuegoForm(None)
        return render(request, 'cliente/busqueda_avanzada_juego.html', {"formulario": formulario})
    except Exception as err:
        logger.error(f'Error en la búsqueda avanzada de juegos: {err}')
        return mi_error_500(request)

def crear_torneo(request):
    try:
        if request.method == 'POST':
            formulario = TorneoForm(request.POST)
            headers = {
                'Authorization': f'Bearer {USER_KEY_ADMINISTRADOR}',
                'Content-Type': 'application/json'
            }
            datos = formulario.data.copy()
            datos["participantes"] = request.POST.getlist("participantes")
            datos["categorias"] = request.POST.getlist("categorias")
            datos["fecha_inicio"] = str(
                datetime.date(year=int(datos['fecha_inicio_year']),
                              month=int(datos['fecha_inicio_month']),
                              day=int(datos['fecha_inicio_day']))
            )
            response = requests.post(
                f'{API_BASE_URL}torneos/crear/',
                headers=headers,
                data=json.dumps(datos)
            )
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Torneo creado exitosamente.')
                return redirect("index")
            else:
                response.raise_for_status()
        else:
            formulario = TorneoForm(None)
        return render(request, 'cliente/create/crear_torneo.html', {"formulario": formulario})
    except HTTPError as http_err:
        logger.error(f'Error al crear el torneo: {http_err}')
        if response.status_code == 400:
            errores = response.json()
            for campo, mensaje in errores.items():
                formulario.add_error(campo, mensaje)
            messages.error(request, 'Error al crear el torneo. Por favor, revisa los errores.')
            return render(request, 'cliente/create/crear_torneo.html', {"formulario": formulario})
        else:
            return mi_error_500(request)
    except Exception as err:
        logger.error(f'Ocurrió un error: {err}')
        formulario.add_error(None, f"Ocurrió un error inesperado: {err}")
        messages.error(request, 'Ocurrió un error inesperado. Por favor, intenta nuevamente.')
        return render(request, 'cliente/create/crear_torneo.html', {"formulario": formulario})

def editar_torneo(request, torneo_id):
    try:
        helper = Helper()
        torneo = helper.obtener_torneo(torneo_id)
        if request.method == "POST":
            formulario = TorneoForm(request.POST)
            if formulario.is_valid():
                datos = request.POST.copy()
                datos["participantes"] = request.POST.getlist("participantes")
                datos["categoria"] = request.POST.get("categoria")
                datos["fecha_inicio"] = str(datetime.date(
                    year=int(datos['fecha_inicio_year']),
                    month=int(datos['fecha_inicio_month']),
                    day=int(datos['fecha_inicio_day'])
                ))
                response = requests.put(
                    f'{API_BASE_URL}torneos/editar/{torneo_id}/',
                    headers={
                        'Authorization': f'Bearer {USER_KEY_ADMINISTRADOR}',
                        'Content-Type': 'application/json'
                    },
                    data=json.dumps(datos)
                )
                if response.status_code == 200:
                    messages.success(request, 'Torneo editado exitosamente.')
                    return redirect("listar_torneos")
                else:
                    if response.status_code == 400:
                        errores = response.json()
                        for campo, mensaje in errores.items():
                            formulario.add_error(campo, mensaje)
                        messages.error(request, 'Error al editar el torneo. Por favor, revisa los errores.')
                    else:
                        response.raise_for_status()
        else:
            formulario = TorneoForm(
                initial={
                    'nombre': torneo['nombre'],
                    'descripcion': torneo["descripcion"],
                    'fecha_inicio': datetime.datetime.strptime(torneo['fecha_inicio'], '%d-%m-%Y').date(),
                    'categoria': torneo['categoria'],
                    'duracion': torneo['duracion'],
                    'participantes': [str(participante['id']) for participante in torneo['participantes']]
                }
            )
        return render(request, 'cliente/create/editar_torneo.html', {"formulario": formulario, "torneo": torneo})
    except Exception as err:
        logger.error(f'Error al editar el torneo: {err}')
        return mi_error_500(request)

def torneo_editar_nombre(request, torneo_id):
    try:
        datosFormulario = None
        if request.method == "POST":
            datosFormulario = request.POST
        helper = Helper()
        torneo = helper.obtener_torneo(torneo_id)
        formulario = TorneoActualizarNombreForm(
            datosFormulario,
            initial={'nombre': torneo['nombre']}
        )
        if request.method == "POST":
            formulario = TorneoActualizarNombreForm(request.POST)
            headers = crear_cabecera()
            datos = {"nombre": request.POST.get("nombre")}
            response = requests.patch(
                f'{API_BASE_URL}torneos/actualizar-nombre/{torneo_id}/',
                headers=headers,
                data=json.dumps(datos)
            )
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Nombre del torneo actualizado exitosamente.')
                return redirect("listar_torneos")
            else:
                response.raise_for_status()
        return render(request, 'cliente/create/actualizar_nombre_torneo.html', {"formulario": formulario, "torneo": torneo})
    except HTTPError as http_err:
        logger.error(f'Error al actualizar el nombre del torneo: {http_err}')
        if response.status_code == 400:
            errores = response.json()
            for error in errores:
                formulario.add_error(error, errores[error])
            messages.error(request, 'Error al actualizar el nombre del torneo. Por favor, revisa los errores.')
            return render(request, 'cliente/create/actualizar_nombre_torneo.html', {"formulario": formulario, "torneo": torneo})
        else:
            return mi_error_500(request)
    except Exception as err:
        logger.error(f'Ocurrió un error: {err}')
        messages.error(request, 'Ocurrió un error inesperado. Por favor, intenta nuevamente.')
        return mi_error_500(request)

def torneo_eliminar(request, torneo_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            f'{API_BASE_URL}torneos/eliminar/{torneo_id}/',
            headers=headers,
        )
        if response.status_code == requests.codes.ok:
            messages.success(request, 'Torneo eliminado exitosamente.')
            return redirect("listar_torneos")
        else:
            response.raise_for_status()
    except Exception as err:
        logger.error(f'Error al eliminar el torneo: {err}')
        messages.error(request, 'Ocurrió un error inesperado. Por favor, intenta nuevamente.')
        return mi_error_500(request)

def crear_juego(request):
    try:
        if request.method == 'POST':
            formulario = JuegoForm(request.POST)
            headers = {
                'Authorization': f'Bearer {USER_KEY_ADMINISTRADOR}',
                'Content-Type': 'application/json'
            }
            if formulario.is_valid():
                datos = formulario.cleaned_data.copy()
                datos["torneos"] = request.POST.getlist("torneos")
                response = requests.post(
                    f'{API_BASE_URL}juegos/crear/',
                    headers=headers,
                    data=json.dumps(datos)
                )
                if response.status_code == requests.codes.ok:
                    messages.success(request, 'Juego creado exitosamente.')
                    return redirect("juegos_lista")
                else:
                    response.raise_for_status()
            else:
                return render(request, 'cliente/create/crear_juego.html', {"formulario": formulario})
        else:
            formulario = JuegoForm(None)
        return render(request, 'cliente/create/crear_juego.html', {"formulario": formulario})
    except HTTPError as http_err:
        logger.error(f'Error al crear el juego: {http_err}')
        if response.status_code == 400:
            errores = response.json()
            for campo, mensaje in errores.items():
                formulario.add_error(campo, mensaje)
            messages.error(request, 'Error al crear el juego. Por favor, revisa los errores.')
            return render(request, 'cliente/create/crear_juego.html', {"formulario": formulario})
        else:
            return mi_error_500(request)
    except Exception as err:
        logger.error(f'Ocurrió un error: {err}')
        formulario.add_error(None, f"Ocurrió un error inesperado: {err}")
        messages.error(request, 'Ocurrió un error inesperado. Por favor, intenta nuevamente.')
        return render(request, 'cliente/create/crear_juego.html', {"formulario": formulario})

def editar_juego(request, juego_id):
    try:
        datosFormulario = None
        if request.method == "POST":
            datosFormulario = request.POST
        helper = Helper()
        juego = helper.obtener_juego(juego_id)
        formulario = JuegoForm(
            datosFormulario,
            initial={
                'nombre': juego['nombre'],
                'descripcion': juego["descripcion"],
                'genero': juego["genero"],
                'id_consola': str(juego['id_consola']),
                'torneo': str(juego['torneo'])
            }
        )
        if request.method == "POST":
            formulario = JuegoForm(request.POST)
            if formulario.is_valid():
                datos = request.POST.copy()
                datos["torneo"] = request.POST.get("torneo")
                datos["id_consola"] = request.POST.get("id_consola")
                response = requests.put(
                    f'{API_BASE_URL}juegos/editar/{juego_id}/',
                    headers={
                        'Authorization': f'Bearer {USER_KEY_ADMINISTRADOR}',
                        'Content-Type': 'application/json'
                    },
                    data=json.dumps(datos)
                )
                if response.status_code == 200:
                    messages.success(request, 'Juego editado exitosamente.')
                    return redirect("juegos_lista")
                else:
                    if response.status_code == 400:
                        errores = response.json()
                        for campo, mensaje in errores.items():
                            formulario.add_error(campo, mensaje)
                        messages.error(request, 'Error al editar el juego. Por favor, revisa los errores.')
                    else:
                        return tratar_errores(request, response.status_code)
        return render(request, 'cliente/create/editar_juego.html', {"formulario": formulario, "juego": juego})
    except Exception as err:
        logger.error(f'Error al editar el juego: {err}')
        return mi_error_500(request)

def juego_editar_nombre(request, juego_id):
    try:
        datosFormulario = None
        if request.method == "POST":
            datosFormulario = request.POST
        helper = Helper()
        juego = helper.obtener_juego(juego_id)
        formulario = JuegoActualizarNombreForm(
            datosFormulario,
            initial={'nombre': juego['nombre']}
        )
        if request.method == "POST":
            formulario = JuegoActualizarNombreForm(request.POST)
            headers = crear_cabecera()
            datos = {"nombre": request.POST.get("nombre")}
            response = requests.patch(
                f'{API_BASE_URL}juegos/actualizar-nombre/{juego_id}/',
                headers=headers,
                data=json.dumps(datos)
            )
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Nombre del juego actualizado exitosamente.')
                return redirect("juegos_lista")
            else:
                response.raise_for_status()
        return render(request, 'cliente/create/actualizar_nombre_juego.html', {"formulario": formulario, "juego": juego})
    except HTTPError as http_err:
        logger.error(f'Error al actualizar el nombre del juego: {http_err}')
        if response.status_code == 400:
            errores = response.json()
            for error in errores:
                formulario.add_error(error, errores[error])
            messages.error(request, 'Error al actualizar el nombre del juego. Por favor, revisa los errores.')
            return render(request, 'cliente/create/actualizar_nombre_juego.html', {"formulario": formulario, "juego": juego})
        else:
            return mi_error_500(request)
    except Exception as err:
        logger.error(f'Ocurrió un error: {err}')
        messages.error(request, 'Ocurrió un error inesperado. Por favor, intenta nuevamente.')
        return mi_error_500(request)

def juego_eliminar(request, juego_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            f'{API_BASE_URL}juegos/eliminar/{juego_id}/',
            headers=headers,
        )
        if response.status_code == requests.codes.ok:
            messages.success(request, 'Juego eliminado exitosamente.')
            return redirect("juegos_lista")
        else:
            response.raise_for_status()
    except Exception as err:
        logger.error(f'Error al eliminar el juego: {err}')
        messages.error(request, 'Ocurrió un error inesperado. Por favor, intenta nuevamente.')
        return mi_error_500(request)

def crear_participante(request):
    try:
        if request.method == 'POST':
            formulario = ParticipanteForm(request.POST)
            headers = {
                'Authorization': f'Bearer {USER_KEY_ADMINISTRADOR}',
                'Content-Type': 'application/json'
            }
            datos = formulario.data.copy()
            datos["fecha_inscripcion"] = str(
                datetime.date(year=int(datos['fecha_inscripcion_year']),
                              month=int(datos['fecha_inscripcion_month']),
                              day=int(datos['fecha_inscripcion_day']))
            )
            datos["equipos"] = request.POST.getlist("equipos")
            response = requests.post(
                f'{API_BASE_URL}participantes/crear/',
                headers=headers,
                data=json.dumps(datos)
            )
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Participante creado exitosamente.')
                return redirect("participantes_lista")
            else:
                response.raise_for_status()
        else:
            formulario = ParticipanteForm(None)
        return render(request, 'cliente/create/crear_participante.html', {"formulario": formulario})
    except HTTPError as http_err:
        logger.error(f'Error al crear el participante: {http_err}')
        if response.status_code == 400:
            errores = response.json()
            for campo, mensaje in errores.items():
                formulario.add_error(campo, mensaje)
            messages.error(request, 'Error al crear el participante. Por favor, revisa los errores.')
            return render(request, 'cliente/create/crear_participante.html', {"formulario": formulario})
        else:
            return mi_error_500(request)
    except Exception as err:
        logger.error(f'Ocurrió un error: {err}')
        formulario.add_error(None, f"Ocurrió un error inesperado: {err}")
        messages.error(request, 'Ocurrió un error inesperado. Por favor, intenta nuevamente.')
        return render(request, 'cliente/create/crear_participante.html', {"formulario": formulario})

def editar_participante(request, participante_id):
    try:
        helper = Helper()
        participante = helper.obtener_participante(participante_id)
        if request.method == "POST":
            formulario = ParticipanteForm(request.POST)
            if formulario.is_valid():
                datos = request.POST.copy()
                datos["equipos"] = request.POST.getlist("equipos")
                datos["fecha_inscripcion"] = str(datetime.date(
                    year=int(datos['fecha_inscripcion_year']),
                    month=int(datos['fecha_inscripcion_month']),
                    day=int(datos['fecha_inscripcion_day'])
                ))
                response = requests.put(
                    f'{API_BASE_URL}participantes/editar/{participante_id}/',
                    headers={
                        'Authorization': f'Bearer {USER_KEY_ADMINISTRADOR}',
                        'Content-Type': 'application/json'
                    },
                    data=json.dumps(datos)
                )
                if response.status_code == 200:
                    messages.success(request, 'Participante editado exitosamente.')
                    return redirect("participantes_lista")
                else:
                    if response.status_code == 400:
                        errores = response.json()
                        for campo, mensaje in errores.items():
                            formulario.add_error(campo, mensaje)
                        messages.error(request, 'Error al editar el participante. Por favor, revisa los errores.')
                    else:
                        return tratar_errores(request, response.status_code)
        else:
            formulario = ParticipanteForm(
                initial={
                    'usuario': participante['usuario'],
                    'puntos_obtenidos': participante["puntos_obtenidos"],
                    'posicion_final': participante["posicion_final"],
                    'fecha_inscripcion': datetime.datetime.strptime(participante['fecha_inscripcion'], '%Y-%m-%d').date(),
                    'tiempo_jugado': participante["tiempo_jugado"],
                    'equipos': [str(equipo['id']) for equipo in participante['equipos']]
                }
            )
        return render(request, 'cliente/create/editar_participante.html', {"formulario": formulario, "participante": participante})
    except Exception as err:
        logger.error(f'Error al editar el participante: {err}')
        return mi_error_500(request)

def participante_editar_equipos(request, participante_id):
    try:
        datosFormulario = None
        if request.method == "POST":
            datosFormulario = request.POST
        helper = Helper()
        participante = helper.obtener_participante(participante_id)
        formulario = ParticipanteActualizarEquiposForm(
            datosFormulario,
            initial={'equipos': [str(equipo['id']) for equipo in participante['equipos']]}
        )
        if request.method == "POST":
            formulario = ParticipanteActualizarEquiposForm(request.POST)
            headers = crear_cabecera()
            datos = {"equipos": request.POST.getlist("equipos")}
            response = requests.patch(
                f'{API_BASE_URL}participantes/actualizar-equipos/{participante_id}/',
                headers=headers,
                data=json.dumps(datos)
            )
            if response.status_code == requests.codes.ok:
                messages.success(request, 'Equipos del participante actualizados exitosamente.')
                return redirect("participantes_lista")
            else:
                response.raise_for_status()
        return render(request, 'cliente/create/actualizar_equipos_participante.html', {"formulario": formulario, "participante": participante})
    except HTTPError as http_err:
        logger.error(f'Error al actualizar los equipos del participante: {http_err}')
        if response.status_code == 400:
            errores = response.json()
            for error in errores:
                formulario.add_error(error, errores[error])
            messages.error(request, 'Error al actualizar los equipos del participante. Por favor, revisa los errores.')
            return render(request, 'cliente/create/actualizar_equipos_participante.html', {"formulario": formulario, "participante": participante})
        else:
            return mi_error_500(request)
    except Exception as err:
        logger.error(f'Ocurrió un error: {err}')
        messages.error(request, 'Ocurrió un error inesperado. Por favor, intenta nuevamente.')
        return mi_error_500(request)

def participante_eliminar(request, participante_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            f'{API_BASE_URL}participantes/eliminar/{participante_id}/',
            headers=headers,
        )
        if response.status_code == requests.codes.ok:
            messages.success(request, 'Participante eliminado exitosamente.')
            return redirect("participantes_lista")
        else:
            response.raise_for_status()
    except Exception as err:
        logger.error(f'Error al eliminar el participante: {err}')
        messages.error(request, 'Ocurrió un error inesperado. Por favor, intenta nuevamente.')
        return mi_error_500(request)

def crear_jugador(request):
    try:
        if request.method == 'POST':
            formulario = JugadorForm(request.POST)
            headers = {
                'Authorization': f'Bearer {USER_KEY_ADMINISTRADOR}',
                'Content-Type': 'application/json'
            }
            if formulario.is_valid():
                datos = formulario.cleaned_data.copy()
                datos["torneos"] = request.POST.getlist("torneos")
                response = requests.post(
                    f'{API_BASE_URL}jugadores/crear/',
                    headers=headers,
                    data=json.dumps(datos)
                )
                if response.status_code == requests.codes.ok:
                    messages.success(request, 'Jugador creado exitosamente.')
                    return redirect("listar_torneos")
                else:
                    response.raise_for_status()
            else:
                return render(request, 'cliente/create/crear_jugador.html', {"formulario": formulario})
        else:
            formulario = JugadorForm(None)
        return render(request, 'cliente/create/crear_jugador.html', {"formulario": formulario})
    except HTTPError as http_err:
        logger.error(f'Error al crear el jugador: {http_err}')
        if response.status_code == 400:
            errores = response.json()
            for campo, mensaje in errores.items():
                formulario.add_error(campo, mensaje)
            messages.error(request, 'Error al crear el jugador. Por favor, revisa los errores.')
            return render(request, 'cliente/create/crear_jugador.html', {"formulario": formulario})
        else:
            return mi_error_500(request)
    except Exception as err:
        logger.error(f'Ocurrió un error: {err}')
        formulario.add_error(None, f"Ocurrió un error inesperado: {err}")
        messages.error(request, 'Ocurrió un error inesperado. Por favor, intenta nuevamente.')
        return render(request, 'cliente/create/crear_jugador.html', {"formulario": formulario})

def editar_jugador(request, jugador_id):
    try:
        helper = Helper()
        jugador = helper.obtener_jugador(jugador_id)
        if request.method == "POST":
            formulario = JugadorForm(request.POST)
            if formulario.is_valid():
                datos = request.POST.copy()
                datos["torneos"] = request.POST.getlist("torneos")
                response = requests.put(
                    f'{API_BASE_URL}jugadores/editar/{jugador_id}/',
                    headers=crear_cabecera(),
                    data=json.dumps(datos)
                )
                if response.status_code == 200:
                    messages.success(request, 'Jugador editado exitosamente.')
                    return redirect("listar_torneos")
                else:
                    if response.status_code == 400:
                        errores = response.json()
                        for campo, mensaje in errores.items():
                            formulario.add_error(campo, mensaje)
                        messages.error(request, 'Error al editar el jugador. Por favor, revisa los errores.')
                    else:
                        return tratar_errores(request, response.status_code)
        else:
            formulario = JugadorForm(
                initial={
                    'usuario': jugador['usuario']['id'],
                    'puntos': jugador["puntos"],
                    'equipo': jugador["equipo"] if jugador["equipo"] else "",
                    'torneos': [str(torneo['id']) for torneo in jugador['torneos']]
                }
            )
        return render(request, 'cliente/create/editar_jugador.html', {"formulario": formulario, "jugador": jugador})
    except Exception as err:
        logger.error(f'Error al editar el jugador: {err}')
        return mi_error_500(request)

def editar_puntos_jugador(request, jugador_id):
    try:
        helper = Helper()
        jugador = helper.obtener_jugador(jugador_id)
        if request.method == "POST":
            formulario = JugadorActualizarPuntosForm(request.POST)
            if formulario.is_valid():
                datos = request.POST.copy()
                response = requests.patch(
                    f'{API_BASE_URL}jugadores/actualizar_puntos/{jugador_id}/',
                    headers=crear_cabecera(),
                    data=json.dumps(datos)
                )
                if response.status_code == 200:
                    messages.success(request, 'Puntos del jugador actualizados exitosamente.')
                    return redirect("listar_torneos")
                else:
                    if response.status_code == 400:
                        errores = response.json()
                        for campo, mensaje in errores.items():
                            formulario.add_error(campo, mensaje)
                        messages.error(request, 'Error al actualizar los puntos del jugador. Por favor, revisa los errores.')
                    else:
                        return tratar_errores(request, response.status_code)
        else:
            formulario = JugadorActualizarPuntosForm(initial={"puntos": jugador["puntos"]})
        return render(request, 'cliente/create/actualizar_puntos_jugador.html', {"formulario": formulario, "jugador": jugador})
    except Exception as err:
        logger.error(f'Error al actualizar los puntos del jugador: {err}')
        return mi_error_500(request)

def jugador_eliminar_torneo(request, jugador_id, torneo_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            f'{API_BASE_URL}jugadores/eliminar/{jugador_id}/{torneo_id}/',
            headers=headers,
        )
        if response.status_code == requests.codes.ok:
            messages.success(request, 'Relación del jugador con el torneo eliminada exitosamente.')
            return redirect("listar_torneos")
        else:
            response.raise_for_status()
    except Exception as err:
        logger.error(f'Error al eliminar la relación del jugador con el torneo: {err}')
        messages.error(request, 'Ocurrió un error inesperado. Por favor, intenta nuevamente.')
        return mi_error_500(request)

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