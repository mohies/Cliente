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


# Configurar el logger
logger = logging.getLogger(__name__)


# Definimos por defecto la version que tenemos de la API y las establecemos en nuestras aplicaciones
API_VERSION = env("API_VERSION", default="v1") 
API_BASE_URL = f'https://mohbenbou.pythonanywhere.com/api/{API_VERSION}/'

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
    helper = Helper()  # Instanciamos el Helper
    
    response = helper.realizar_peticion(
        metodo='GET',
        url=f'{API_BASE_URL}torneos/mejorada/',
        request=request
    )

    torneos = response.json()
    
    return render(request, 'cliente/lista_api.html', {"torneos_mostrar": torneos})

def participantes_lista_api(request):
    helper = Helper()  # Instanciamos el Helper
    
    response = helper.realizar_peticion(
        metodo='GET',
        url=f'{API_BASE_URL}participantes/mejorada/',
        request=request
    )

    participantes = response.json()
    
    return render(request, 'cliente/lista_participantes.html', {"participantes_mostrar": participantes})

def juegos_lista_api(request):
    helper = Helper()  # Instanciamos el Helper
    
    response = helper.realizar_peticion(
        metodo='GET',
        url=f'{API_BASE_URL}juegos/mejorada/',
        request=request
    )

    juegos = response.json()
    
    return render(request, 'cliente/lista_juegos.html', {"juegos_mostrar": juegos})


def equipos_lista_api(request):
    helper = Helper()  # Instanciamos el Helper
    
    response = helper.realizar_peticion(
        metodo='GET',
        url=f'{API_BASE_URL}equipos/',
        request=request
    )

    equipos = response.json()
    
    return render(request, 'cliente/lista_equipos.html', {"equipos_mostrar": equipos})


def torneo_busqueda_simple(request):
    helper = Helper()  # Instanciamos el Helper
    
    # Creamos el formulario con los datos GET de la solicitud
    formulario = BusquedaTorneoForm(request.GET or None)
    
    # Verificamos si el formulario es válido
    if formulario.is_valid():
        params = formulario.cleaned_data
        
        # Realizamos la petición a la API utilizando el Helper
        response = helper.realizar_peticion(
            metodo='GET',
            url=f'{API_BASE_URL}torneos/buscar/',
            params={'textoBusqueda': params.get("textoBusqueda")},  # Pasamos el texto de búsqueda
            request=request
        )

        # Procesamos la respuesta
        torneos = process_response(response)
        
        # Renderizamos la respuesta con la lista de torneos
        return render(request, 'cliente/lista_api.html', {"torneos_mostrar": torneos})
    
    # Si el formulario no es válido o no se realiza una búsqueda, redirigimos a la página de búsqueda
    if "HTTP_REFERER" in request.META:
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")



def torneo_busqueda_avanzada(request):
    helper = Helper()  # 🔥 Instanciamos el Helper
    formulario = BusquedaAvanzadaTorneoForm(request.GET or None)
    
    if formulario.is_valid():
        params = formulario.cleaned_data
    
        response = helper.realizar_peticion(
            metodo='GET',
            url=f'{API_BASE_URL}torneos/buscar/avanzado/',
            params=params,  # ✅ ¡Aquí está el cambio!
            request=request
        )

        torneos = process_response(response)
        return render(request, 'cliente/lista_api.html', {"torneos_mostrar": torneos})
    
    return render(request, 'cliente/busqueda_avanzada.html', {"formulario": formulario})



def equipo_busqueda_avanzada(request):
    helper = Helper()  
    formulario = BusquedaAvanzadaEquipoForm(request.GET or None)

    if formulario.is_valid():
        params = formulario.cleaned_data
        
        response = helper.realizar_peticion(
            metodo='GET',
            url=f'{API_BASE_URL}equipos/buscar/avanzado/',
            params=params,
            request=request
        )

        if response.status_code == requests.codes.ok:
            equipos = process_response(response)
            return render(request, 'cliente/lista_equipos.html', {"equipos_mostrar": equipos})

        if response.status_code == 400:
            return helper.manejar_error_400(response, formulario, 'cliente/busqueda_avanzada_equipo.html', request)

        return tratar_errores(request, response.status_code)

    return render(request, 'cliente/busqueda_avanzada_equipo.html', {"formulario": formulario})

def participante_busqueda_avanzada(request):
    helper = Helper()  
    formulario = BusquedaAvanzadaParticipanteForm(request.GET or None)

    if formulario.is_valid():
        params = formulario.cleaned_data
        
        response = helper.realizar_peticion(
            metodo='GET',
            url=f'{API_BASE_URL}participantes/buscar/avanzado/',
            params=params,
            request=request
        )

        if response.status_code == requests.codes.ok:
            participantes = process_response(response)
            return render(request, 'cliente/lista_participantes.html', {"participantes_mostrar": participantes})

        if response.status_code == 400:
            return helper.manejar_error_400(response, formulario, 'cliente/busqueda_avanzada_participante.html', request)

        return tratar_errores(request, response.status_code)

    return render(request, 'cliente/busqueda_avanzada_participante.html', {"formulario": formulario})


def juego_busqueda_avanzada(request):
    helper = Helper()  
    formulario = BusquedaAvanzadaJuegoForm(request.GET or None)

    if formulario.is_valid():
        params = formulario.cleaned_data
        
        response = helper.realizar_peticion(
            metodo='GET',
            url=f'{API_BASE_URL}juegos/buscar/avanzado/',
            params=params,
            request=request
        )

        if response.status_code == requests.codes.ok:
            juegos = process_response(response)
            return render(request, 'cliente/lista_juegos.html', {"juegos_mostrar": juegos})

        if response.status_code == 400:
            return helper.manejar_error_400(response, formulario, 'cliente/busqueda_avanzada_juego.html', request)

        return tratar_errores(request, response.status_code)

    return render(request, 'cliente/busqueda_avanzada_juego.html', {"formulario": formulario})


"""
    Realizar las operaciones de POST, PUT, PATCH y DELETE de un modelo, con sus validaciones(al menos 3 campos), control de errores y respuestas.
    (1 punto ,0,25:POST, 0,25: PUT, 0,25:PATCH, 0,25-DELETE)
    
    Incluir en la aplicación algún modelo(Puede repetirse con alguno de los anteriores) un campo que sea un archivo, y 
    gestionar las peticiones GET, POST, PUT, PATCH y DELETE de ese campo(1 punto)
"""
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
    response = helper.realizar_peticion(
        metodo='GET', 
        url=f'{API_BASE_URL}torneos/{torneo_id}/', 
        request=request
    )
    
    torneo = response.json()
    imagen = torneo.get('imagen', None)
    
    if request.method == "POST":
        formulario = TorneoActualizarImagenForm(request.POST, request.FILES)
        
        if formulario.is_valid():
            imagen = request.FILES.get("imagen", None)
            archivos = imagen and {"imagen": imagen}
            
            response = helper.realizar_peticion(
                metodo='PATCH-FILE',
                url=f'{API_BASE_URL}torneos/actualizar-imagen/{torneo_id}/',
                archivos=archivos,
                request=request
            )
            
            resultado = helper.procesar_respuesta(
                request, 
                response, 
                formulario, 
                "Imagen del torneo actualizada exitosamente.", 
                "listar_torneos"
            )
            
            if resultado:
                return resultado
        
    else:
        formulario = TorneoActualizarImagenForm(initial={'imagen': imagen})
    
    return render(
        request, 
        'cliente/create/actualizar_imagen_torneo.html', 
        {"formulario": formulario, "torneo": torneo}
    )




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
    
    return helper.procesar_respuesta(
        request, 
        response, 
        exito_msg="Imagen del torneo eliminada exitosamente.", 
        redirect_url="listar_torneos"
    )


"""
    Realizar las operaciones de POST, PUT, PATCH y DELETE de un modelo con relaciones ManyToOne con sus validaciones(al menos 3 campos), 
    control de errores y respuestas.(1 punto ,0,25:POST, 0,25: PUT, 0,25:PATCH, 0,25-DELETE)
"""

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


"""
  Realizar las operaciones de POST, PUT, PATCH y DELETE de un modelo con una relacion ManyToMany distinto al anterior,con sus validaciones
  (al menos 3 campos), control de errores y respuestas.(1 punto ,0,25:POST, 0,25: PUT, 0,25:PATCH, 0,25-DELETE)
"""
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

"""
Realizar las operaciones de POST, PUT, PATCH y DELETE de un modelo con relaciones ManyToMany con tabla intermedia distinto al anterior, 
con sus validaciones(al menos 3 campos), control de errores y respuestas.(1 punto ,0,25:POST, 0,25: PUT, 0,25:PATCH, 0,25-DELETE)
"""
def crear_jugador(request):
    """
    Vista del cliente para inscribir al usuario autenticado en torneos.
    """
    helper = Helper()  

    if request.method == 'POST':
        formulario = JugadorForm(request.POST)

        if formulario.is_valid():
            # Copiar datos del formulario
            datos = formulario.cleaned_data.copy()

            # Extraer los torneos seleccionados
            datos["torneos"] = request.POST.getlist("torneos")

            # Verificar los datos antes de enviar la solicitud
            print(f"Datos enviados al backend: {datos}")  # Verificar si los datos son correctos

            # Enviar la petición al backend (no mandamos usuario porque ya lo gestionamos con el token)
            response = helper.realizar_peticion(
                metodo='POST',
                url=f'{API_BASE_URL}jugadores/crear/',
                datos=datos,
                request=request
            )

            # Procesar la respuesta
            resultado = helper.procesar_respuesta(
                request, 
                response, 
                formulario, 
                "¡Te has inscrito a los torneos exitosamente!", 
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



def test_cors_view(request):
    return render(request, "test_cors.html")


def registrar_usuario(request):
    helper = Helper() 

    if request.method == 'POST':
        formulario = RegistroForm(request.POST)

        if formulario.is_valid():
            datos = formulario.cleaned_data.copy()
            print("Datos enviados al servidor:", datos)  
            
            response = helper.realizar_peticion(
                metodo='POST',
                url=f'{API_BASE_URL}registrar/usuario/',
                datos=datos,
                request=request
            )

            resultado = helper.procesar_respuesta(
                request, 
                response, 
                formulario, 
                "Usuario registrado exitosamente.", 
                "index"
            )

            if resultado:
                return resultado
        
    else:
        formulario = RegistroForm()

    return render(request, 'cliente/registration/signup.html', {"formulario": formulario})



import requests
from django.shortcuts import render, redirect
from django.contrib import messages

def login(request):
    if request.method == "POST":
        formulario = LoginForm(request.POST)
        
        try:
            usuario = formulario.data.get("usuario")
            password = formulario.data.get("password")

            # 1️ Solicitar el token de acceso
            token_url = 'https://mohbenbou.pythonanywhere.com/oauth2/token/'
            datos = {
                'grant_type': 'password',
                'username': usuario,
                'password': password,
                'client_id': 'pepeid',
                'client_secret': 'pepesecreto',
            }
            response = requests.post(token_url, data=datos)

            # 2️ Verificar si las credenciales son correctas
            if response.status_code == 200:
                token_acceso = response.json().get('access_token')
                request.session["token"] = token_acceso  # Guardamos el token en la sesión

                # 3️ Obtener información del usuario autenticado
                headers = {'Authorization': f'Bearer {token_acceso}'}
                user_response = requests.get(f'https://mohbenbou.pythonanywhere.com/api/v1/usuario/token/{token_acceso}/', headers=headers)

                if user_response.status_code == 200:
                    usuario_data = user_response.json()
                    print("Datos del usuario obtenidos:", usuario_data)  # Debug

                    #  Guardar datos en la sesión 
                    request.session["is_authenticated"] = True
                    request.session["user_id"] = usuario_data.get("id")  
                    request.session["username"] = usuario_data.get("username")  
                    request.session["email"] = usuario_data.get("email")
                    request.session["user_rol"] = usuario_data.get("rol")  

                    messages.success(request, "Inicio de sesión exitoso.")
                    return redirect("index")
                else:
                    messages.error(request, "No se pudo obtener la información del usuario.")
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")

        except Exception as e:
            print(f' Error en la petición: {e}')
            messages.error(request, "Error interno en el servidor. Inténtalo de nuevo.")
        
    else:
        formulario = LoginForm()

    return render(request, 'cliente/registration/login.html', {'form': formulario})



def logout(request):
    request.session.flush()  # Borra toda la sesión y `is_authenticated`
    return redirect('index')


def torneos_usuario_view(request):
    """
    Vista en el cliente que obtiene y muestra los torneos del usuario autenticado.
    """
    helper = Helper()  # Instancia el Helper
    torneos = helper.obtener_torneos_usuario(request)  # Obtiene los torneos desde la API
    
    if torneos is None:
        return render(request, "cliente/error.html", {"mensaje": "Error al obtener torneos o usuario no autenticado"})

    return render(request, "cliente/torneos_usuario.html", {"torneos": torneos})


def torneos_usuario_con_jugadores_view(request):
    """
     Vista en el cliente que obtiene y muestra los torneos del usuario autenticado
     junto con los jugadores en cada torneo.
    """
    helper = Helper()  # Instancia el Helper
    torneos = helper.obtener_torneos_usuario_con_jugadores(request)  # Obtiene los torneos desde la API

    if torneos is None:
        return render(request, "cliente/error.html", {"mensaje": "Error al obtener torneos o usuario no autenticado"})

    return render(request, "cliente/torneos_usuario_jugadores.html", {"torneos": torneos})














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