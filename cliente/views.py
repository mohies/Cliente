import base64
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
    helper = Helper()  # Instanciamos el Helper
    
    if request.method == 'POST':
        formulario = TorneoForm(request.POST)
        
        if formulario.is_valid():
            datos = formulario.data.copy()
            datos["participantes"] = request.POST.getlist("participantes")
            datos["categorias"] = request.POST.getlist("categorias")
            datos["fecha_inicio"] = str(
                datetime.date(
                    year=int(datos['fecha_inicio_year']),
                    month=int(datos['fecha_inicio_month']),
                    day=int(datos['fecha_inicio_day'])
                )
            )
            if 'imagen' in request.FILES:
                imagen = request.FILES["imagen"]
                datos["imagen"] = base64.b64encode(imagen.read()).decode('utf-8')
            
      
            response = helper.realizar_peticion(
                metodo='POST',
                url=f'{API_BASE_URL}torneos/crear/',
                datos=datos,
                request=request
            )     

         
            resultado = helper.procesar_respuesta(request, response, formulario, "Torneo creado exitosamente.", "index")
            
            if resultado:
                return resultado
        
    else:
        formulario = TorneoForm()
    
    return render(request, 'cliente/create/crear_torneo.html', {"formulario": formulario})



def editar_torneo(request, torneo_id):
    helper = Helper()  
    response = helper.realizar_peticion('GET', f'{API_BASE_URL}torneos/{torneo_id}/', request=request)
    torneo = response.json()
    
    if request.method == "POST":
        formulario = TorneoForm(request.POST)
        
        if formulario.is_valid():
            datos = formulario.data.copy()
            datos["participantes"] = request.POST.getlist("participantes")
            datos["categoria"] = request.POST.get("categoria")
            datos["fecha_inicio"] = str(
                datetime.date(
                    year=int(datos['fecha_inicio_year']),
                    month=int(datos['fecha_inicio_month']),
                    day=int(datos['fecha_inicio_day'])
                )
            )
            
            response = helper.realizar_peticion(
                metodo='PUT',
                url=f'{API_BASE_URL}torneos/editar/{torneo_id}/',
                datos=datos,
                request=request
            )
            
            resultado = helper.procesar_respuesta(request, response, formulario, "Torneo editado exitosamente.", "listar_torneos")
            
            if resultado:
                return resultado
        
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



def torneo_editar_nombre(request, torneo_id):
    helper = Helper()
    response = helper.realizar_peticion('GET', f'{API_BASE_URL}torneos/{torneo_id}/', request=request)
    torneo = response.json()
    
    if request.method == "POST":
        formulario = TorneoActualizarNombreForm(request.POST)
        
        if formulario.is_valid():
            datos = {"nombre": request.POST.get("nombre")}
            
            response = helper.realizar_peticion(
                metodo='PATCH',
                url=f'{API_BASE_URL}torneos/actualizar-nombre/{torneo_id}/',
                datos=datos,
                request=request
            )
            
            resultado = helper.procesar_respuesta(request, response, formulario, "Nombre del torneo actualizado exitosamente.", "listar_torneos")
            
            if resultado:
                return resultado
        
    else:
        formulario = TorneoActualizarNombreForm(
            initial={'nombre': torneo['nombre']}
        )
    
    return render(request, 'cliente/create/actualizar_nombre_torneo.html', {"formulario": formulario, "torneo": torneo})

def torneo_actualizar_imagen(request, torneo_id):
    helper = Helper()
    response = helper.realizar_peticion('GET', f'{API_BASE_URL}torneos/{torneo_id}/', request=request)
    torneo = response.json()
    
    if request.method == "POST":
        formulario = TorneoActualizarImagenForm(request.POST, request.FILES)
        
        if formulario.is_valid():
            imagen = request.FILES.get("imagen", None)
            archivos = {'imagen': (imagen.name, imagen, imagen.content_type)} if imagen else None
            
            response = helper.realizar_peticion(
                metodo='PATCH-FILE',
                url=f'{API_BASE_URL}torneos/actualizar-imagen/{torneo_id}/',
                archivos=archivos,
                request=request
            )
            
            resultado = helper.procesar_respuesta(request, response, formulario, "Imagen del torneo actualizada exitosamente.", "listar_torneos")
            
            if resultado:
                return resultado
        
    else:
        formulario = TorneoActualizarImagenForm(initial={'imagen': torneo['imagen']})
    
    return render(request, 'cliente/create/actualizar_imagen_torneo.html', {"formulario": formulario, "torneo": torneo})


def torneo_eliminar(request, torneo_id):
    helper = Helper()
    
    response = helper.realizar_peticion(
        metodo='DELETE',
        url=f'{API_BASE_URL}torneos/eliminar/{torneo_id}/',
        request=request
    )
    
    resultado = helper.procesar_respuesta(request, response, None, "Torneo eliminado exitosamente.", "listar_torneos")
    
    if resultado:
        return resultado

    

def torneo_eliminar_imagen(request, torneo_id):
    helper = Helper()
    
    response = helper.realizar_peticion(
        metodo='DELETE',
        url=f'{API_BASE_URL}torneos/eliminar-imagen/{torneo_id}/',
        request=request
    )
    
    resultado = helper.procesar_respuesta(
        request, 
        response, 
        exito_msg="Imagen del torneo eliminada exitosamente.", 
        redirect_url="listar_torneos"
    )
    
    if resultado:
        return resultado
    
    return mi_error_500(request)



def crear_juego(request):
    helper = Helper()  
    
    if request.method == 'POST':
        formulario = JuegoForm(request.POST)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data.copy()
            datos["torneos"] = request.POST.getlist("torneos")
            
            response = helper.realizar_peticion(
                metodo='POST',
                url=f'{API_BASE_URL}juegos/crear/',
                datos=datos,
                request=request
            )     

            resultado = helper.procesar_respuesta(request, response, formulario, "Juego creado exitosamente.", "juegos_lista")
            
            if resultado:
                return resultado
        
    else:
        formulario = JuegoForm()
    
    return render(request, 'cliente/create/crear_juego.html', {"formulario": formulario})


def editar_juego(request, juego_id):
    helper = Helper()
    juego = helper.realizar_peticion(
        metodo='GET', 
        url=f'{API_BASE_URL}juegos/{juego_id}/', 
        request=request
    ).json()
    
    if request.method == "POST":
        formulario = JuegoForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.copy()
            datos["torneo"] = request.POST.get("torneo")
            datos["id_consola"] = request.POST.get("id_consola")
            
            response = helper.realizar_peticion(
                metodo='PUT',
                url=f'{API_BASE_URL}juegos/editar/{juego_id}/',
                datos=datos,
                request=request
            )     

            resultado = helper.procesar_respuesta(request, response, formulario, "Juego editado exitosamente.", "juegos_lista")
            
            if resultado:
                return resultado
        
    else:
        formulario = JuegoForm(
            initial={
                'nombre': juego['nombre'],
                'descripcion': juego["descripcion"],
                'genero': juego["genero"],
                'id_consola': str(juego['id_consola']),
                'torneo': str(juego['torneo'])
            }
        )
    
    return render(request, 'cliente/create/editar_juego.html', {"formulario": formulario, "juego": juego})


def juego_editar_nombre(request, juego_id):
    helper = Helper()
    juego = helper.realizar_peticion(
        metodo='GET', 
        url=f'{API_BASE_URL}juegos/{juego_id}/', 
        request=request
    ).json()
    
    if request.method == "POST":
        formulario = JuegoActualizarNombreForm(request.POST)
        if formulario.is_valid():
            datos = {"nombre": request.POST.get("nombre")}
            
            response = helper.realizar_peticion(
                metodo='PATCH',
                url=f'{API_BASE_URL}juegos/actualizar-nombre/{juego_id}/',
                datos=datos,
                request=request
            )     

            resultado = helper.procesar_respuesta(request, response, formulario, "Nombre del juego actualizado exitosamente.", "juegos_lista")
            
            if resultado:
                return resultado
        
    else:
        formulario = JuegoActualizarNombreForm(
            initial={'nombre': juego['nombre']}
        )
    
    return render(request, 'cliente/create/actualizar_nombre_juego.html', {"formulario": formulario, "juego": juego})


def juego_eliminar(request, juego_id):
    helper = Helper()
    
    response = helper.realizar_peticion(
        metodo='DELETE',
        url=f'{API_BASE_URL}juegos/eliminar/{juego_id}/',
        request=request
    )

    resultado = helper.procesar_respuesta(request, response, exito_msg="Juego eliminado exitosamente.", redirect_url="juegos_lista")
    
    if resultado:
        return resultado
    
    return redirect('mi_error_500')

def crear_participante(request):
    helper = Helper()

    if request.method == 'POST':
        formulario = ParticipanteForm(request.POST)
        
        if formulario.is_valid():
            datos = formulario.data.copy()
            datos["fecha_inscripcion"] = str(
                datetime.date(
                    year=int(datos['fecha_inscripcion_year']),
                    month=int(datos['fecha_inscripcion_month']),
                    day=int(datos['fecha_inscripcion_day'])
                )
            )
            datos["equipos"] = request.POST.getlist("equipos")
            
            response = helper.realizar_peticion(
                metodo='POST',
                url=f'{API_BASE_URL}participantes/crear/',
                datos=datos,
                request=request
            )
            
            resultado = helper.procesar_respuesta(request, response, formulario, "Participante creado exitosamente.", "participantes_lista")
            
            if resultado:
                return resultado
    
    else:
        formulario = ParticipanteForm()
    
    return render(request, 'cliente/create/crear_participante.html', {"formulario": formulario})


def editar_participante(request, participante_id):
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
            
            response = helper.realizar_peticion(
                metodo='PUT',
                url=f'{API_BASE_URL}participantes/editar/{participante_id}/',
                datos=datos,
                request=request
            )
            
            resultado = helper.procesar_respuesta(request, response, formulario, "Participante editado exitosamente.", "participantes_lista")
            
            if resultado:
                return resultado
    
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


def participante_editar_equipos(request, participante_id):
    helper = Helper()
    participante = helper.obtener_participante(participante_id)
    
    if request.method == "POST":
        formulario = ParticipanteActualizarEquiposForm(request.POST)
        
        if formulario.is_valid():
            datos = {"equipos": request.POST.getlist("equipos")}
            
            response = helper.realizar_peticion(
                metodo='PATCH',
                url=f'{API_BASE_URL}participantes/actualizar-equipos/{participante_id}/',
                datos=datos,
                request=request
            )
            
            resultado = helper.procesar_respuesta(
                request, 
                response, 
                formulario, 
                "Equipos del participante actualizados exitosamente.", 
                "participantes_lista"
            )
            
            if resultado:
                return resultado
    
    else:
        formulario = ParticipanteActualizarEquiposForm(
            initial={'equipos': [str(equipo['id']) for equipo in participante['equipos']]}
        )
    
    return render(request, 'cliente/create/actualizar_equipos_participante.html', {"formulario": formulario, "participante": participante})


def participante_eliminar(request, participante_id):
    helper = Helper()

    response = helper.realizar_peticion(
        metodo='DELETE',
        url=f'{API_BASE_URL}participantes/eliminar/{participante_id}/',
        request=request
    )
    
    resultado = helper.procesar_respuesta(
        request, 
        response, 
        exito_msg="Participante eliminado exitosamente.", 
        redirect_url="participantes_lista"
    )
    
    if resultado:
        return resultado
    
    return mi_error_500(request)


def crear_jugador(request):
    helper = Helper()  
    
    if request.method == 'POST':
        formulario = JugadorForm(request.POST)
        
        if formulario.is_valid():
            datos = formulario.cleaned_data.copy()
            datos["torneos"] = request.POST.getlist("torneos")
            
            response = helper.realizar_peticion(
                metodo='POST',
                url=f'{API_BASE_URL}jugadores/crear/',
                datos=datos,
                request=request
            )
            
            resultado = helper.procesar_respuesta(
                request, 
                response, 
                formulario, 
                "Jugador creado exitosamente.", 
                "listar_torneos"
            )
            
            if resultado:
                return resultado
        
    else:
        formulario = JugadorForm()
    
    return render(request, 'cliente/create/crear_jugador.html', {"formulario": formulario})


def editar_jugador(request, jugador_id):
    helper = Helper()
    jugador = helper.obtener_jugador(jugador_id)
    
    if request.method == "POST":
        formulario = JugadorForm(request.POST)
        
        if formulario.is_valid():
            datos = request.POST.copy()
            datos["torneos"] = request.POST.getlist("torneos")
            
            response = helper.realizar_peticion(
                metodo='PUT',
                url=f'{API_BASE_URL}jugadores/editar/{jugador_id}/',
                datos=datos,
                request=request
            )
            
            resultado = helper.procesar_respuesta(
                request, 
                response, 
                formulario, 
                "Jugador editado exitosamente.", 
                "listar_torneos"
            )
            
            if resultado:
                return resultado
    
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


def editar_puntos_jugador(request, jugador_id):
    helper = Helper()
    jugador = helper.obtener_jugador(jugador_id)
    
    if request.method == "POST":
        formulario = JugadorActualizarPuntosForm(request.POST)
        
        if formulario.is_valid():
            datos = request.POST.copy()
            
            response = helper.realizar_peticion(
                metodo='PATCH',
                url=f'{API_BASE_URL}jugadores/actualizar_puntos/{jugador_id}/',
                datos=datos,
                request=request
            )
            
            resultado = helper.procesar_respuesta(
                request, 
                response, 
                formulario, 
                "Puntos del jugador actualizados exitosamente.", 
                "listar_torneos"
            )
            
            if resultado:
                return resultado
    
    else:
        formulario = JugadorActualizarPuntosForm(initial={"puntos": jugador["puntos"]})
    
    return render(request, 'cliente/create/actualizar_puntos_jugador.html', {"formulario": formulario, "jugador": jugador})


def jugador_eliminar_torneo(request, jugador_id, torneo_id):
    helper = Helper()
    
    response = helper.realizar_peticion(
        metodo='DELETE',
        url=f'{API_BASE_URL}jugadores/eliminar/{jugador_id}/{torneo_id}/',
        request=request
    )
    
    resultado = helper.procesar_respuesta(
        request, 
        response, 
        exito_msg="Relación del jugador con el torneo eliminada exitosamente.", 
        redirect_url="listar_torneos"
    )
    
    if resultado:
        return resultado
    
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