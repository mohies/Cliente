import json
from django.shortcuts import redirect, render
import requests
import environ
import os
import xml.etree.ElementTree as ET
import logging
from django.contrib import messages
from requests.exceptions import HTTPError
import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
logger = logging.getLogger(__name__)

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
def crear_cabecera(request=None):
    """
    Crea y devuelve una cabecera con el token de autenticación de la sesión.
    - Usa el token de la sesión si está disponible.
    - Si no hay token en la sesión, obtiene uno nuevo y lo almacena.
    """

    if request and hasattr(request, 'session'):
        token = request.session.get("token")  # 🔹 Intentamos obtener el token de la sesión

        if token:
            return {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }

    #  Si no hay token en la sesión, obtenemos uno nuevo
    token_url = f'{API_BASE_TOKEN}oauth2/token/'
    datos = {
        'grant_type': 'password',
        'username': 'javier',  
        'password': 'elpepe34',  
        'client_id': 'pepeid',
        'client_secret': 'pepesecreto',
    }

    response = requests.post(token_url, data=datos)

    if response.status_code == 200:
        token = response.json().get('access_token')

        # Guardamos el nuevo token en la sesión, si es posible
        if request and hasattr(request, 'session'):
            request.session["token"] = token  

        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    # ❌ Si no se pudo obtener un token, devolvemos una cabecera sin autenticación
    return {
        'Content-Type': 'application/json'
    }

"""
def crear_cabecera2():
    helper = Helper()

    # Si ya tenemos el token, lo usamos
    if helper.token:
        return {
            'Authorization': f'Bearer {helper.token}',
            'Content-Type': 'application/x-www-form-urlencoded'  # Cambiamos el tipo de contenido
        }

    # Si no hay token, obtenemos uno nuevo
    token_url = f'{API_BASE_TOKEN}oauth2/token/'
    datos = {
        'grant_type': 'password',
        'username': 'admin',  
        'password': 'admin',  
        'client_id': 'pepeid',
        'client_secret': 'pepesecreto',
    }

    # Solicitamos el token directamente
    response = requests.post(token_url, data=datos)
    
    # Solo manejamos el caso exitoso (200)
    token = response.json().get('access_token')
    helper.token = token  # Guardamos el token para futuras peticiones
    
    return {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/x-www-form-urlencoded'  # Cambiamos el tipo de contenido
    }

"""


env = environ.Env()

# Construye el path de BASE_DIR 
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carga las variables del archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

API_VERSION = env("API_VERSION", default="v1") 
API_BASE_URL = f'https://mohbenbou.pythonanywhere.com/api/{API_VERSION}/'
API_BASE_TOKEN = f'https://mohbenbou.pythonanywhere.com/'

class Helper:
    
    token = None
    
    def obtener_participantes_select(self):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}participantes/', headers=headers)
        participantes = response.json()
        
        return [(participante['id'], participante['usuario']['nombre']) for participante in participantes]

    def obtener_categorias_select(self):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}categorias/', headers=headers)
        print("RESPUESTA API:", response)  # Para ver qué está devolviendo realmente

        categorias = response.json()
        return [(categoria, categoria) for categoria in categorias]  # Devuelve tuplas (nombre, nombre)
    
    def obtener_torneo(self, torneo_id):
        """
        Obtiene los datos de un torneo específico desde la API.
        """
        headers = crear_cabecera()  # Usa la misma estructura de las otras funciones
        response = requests.get(f'{API_BASE_URL}torneos/{torneo_id}/', headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al obtener el torneo {torneo_id}: {response.status_code}")
        
        
    def obtener_torneos_select(self):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}torneos/', headers=headers)
        torneos = response.json()
        return [(torneo['id'], torneo['nombre']) for torneo in torneos]

    def obtener_consolas_select(self):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}consolas/', headers=headers)
        consolas = response.json()
        return [(consola['id'], consola['nombre']) for consola in consolas]
    
    
    
    def obtener_juego(self, juego_id):
        """
        Obtiene los datos de un juego específico desde la API.
        """
        headers = crear_cabecera()  # Usa la misma estructura de las otras funciones
        response = requests.get(f'{API_BASE_URL}juegos/{juego_id}/', headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al obtener el juego {juego_id}: {response.status_code}")
        

    def obtener_usuarios_select(self):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}usuarios/', headers=headers)
        usuarios = response.json()
        return [(usuario['id'], usuario['nombre']) for usuario in usuarios]

    def obtener_equipos_select(self):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}equipos/', headers=headers)
        equipos = response.json()
        return [(equipo['id'], equipo['nombre']) for equipo in equipos]
    
    
    def obtener_participante(self, participante_id):
        """
        Obtiene los datos de un participante específico desde la API.
        """
        headers = crear_cabecera()  # Usa la misma estructura de las otras funciones
        response = requests.get(f'{API_BASE_URL}participantes/{participante_id}/', headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error al obtener el participante {participante_id}: {response.status_code}")

    def obtener_usuarioslogin_select(self):
        """
        Obtiene la lista de usuarios registrados y los devuelve en formato (id, username).
        """
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}usuarios-login/', headers=headers)

        if response.status_code == 200:
            usuarios = response.json()
            return [(usuario['id'], usuario['username']) for usuario in usuarios]  
        
        return [] 
    
    def obtener_torneos_select(self):
        """
        Obtiene la lista de torneos disponibles y los devuelve en formato (id, nombre).
        """
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}torneos/', headers=headers)

        if response.status_code == 200:
            torneos = response.json()
            return [(torneo['id'], torneo['nombre']) for torneo in torneos]  # Retorna una lista de tuplas
        return []  # Si hay error, retorna lista vacía

    def obtener_jugador(self, jugador_id):
        """
        Obtiene los detalles de un jugador desde la API.
        """
        response = requests.get(f'{API_BASE_URL}jugadores/obtener/{jugador_id}/', headers=crear_cabecera())

        if response.status_code == 200:
            return response.json()
        return None  # Devuelve None si falla la petición
    
    def obtener_torneos_usuario(self, request):
        """
        Obtiene los torneos en los que el usuario autenticado está inscrito.
        """
        headers = crear_cabecera(request)  # Usa el token de la sesión
        url = f"{API_BASE_URL}torneos/mis-torneos/"  # 🔹 Asegúrate de que la URL es correcta
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error al obtener los torneos del usuario: {response.status_code} - {response.text}")
            return None
    
    def obtener_torneos_usuario_con_jugadores(self, request):
        """
        🔹 Obtiene los torneos en los que el usuario autenticado está inscrito,
        junto con la lista de jugadores en cada torneo.
        """
        headers = crear_cabecera(request)  # Usa el token de la sesión
        url = f"{API_BASE_URL}torneos/mis-torneos-jugadores/"  # 🔹 Endpoint correcto
        
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error al obtener torneos y jugadores: {response.status_code} - {response.text}")
            return None

    
   
   
    """
    Incluir mensajes en la aplicación de cliente, para indicar que se ha realizado cada operación correctamente (1 punto)
    Controlar correctamente los errores tanto en cliente como en la API, para que aparezca por consola siempre el error que se produce, pero por la aplicación 
    te rediriga a las páginas de errores correspondiente(1 punto)
    Refactorizar el código, para que sólo se controle errores, se hagan las peticiones y se gestionen las respuesta desde la clase helper(1 punto)"""
    
    
    def realizar_peticion(self, metodo, url, datos=None, params=None, archivos=None, request=None):
        """
        Método genérico para realizar peticiones HTTP, manejar errores y mostrar mensajes de éxito.
        """
        headers = crear_cabecera(request)
        try:

            if metodo == 'GET':
                response = requests.get(url, headers=headers, params=params)
            elif metodo == 'POST':
                response = requests.post(url, headers=headers, data=json.dumps(datos))
            elif metodo == 'PUT':
                response = requests.put(url, headers=headers, data=json.dumps(datos))
            elif metodo == 'PATCH':
                response = requests.patch(url, headers=headers, data=json.dumps(datos))
            elif metodo == 'DELETE':
                response = requests.delete(url, headers=headers)
            elif metodo == 'PATCH-FILE':         
                response = requests.patch(url, files=archivos) # Le quitamos el header porque no es necesario en este caso ya que sobrescribe el contenttype que requests ha establecido y lo intentara leer el header como texto JSON
            else:
                raise ValueError("Método HTTP no soportado.")
            
            response.raise_for_status()  # Lanza excepción para errores HTTP
            return response
        
        except HTTPError as http_err:
            #   mostramos el detalle de la respuesta
            if http_err.response is not None:
                try:
                    errores_json = http_err.response.json()
                    logger.error(f'Error HTTP {http_err.response.status_code}: {errores_json}')
                except ValueError:
                    logger.error(f'Error HTTP {http_err.response.status_code}: {http_err.response.text}')
            else:
                logger.error(f'Error HTTP sin respuesta: {http_err}')
            
       
            return http_err.response
        
        except (ConnectionError, requests.Timeout) as conn_err:
            logger.error(f'Error de conexión o timeout: {conn_err}')
            if requests.request:
                messages.error(requests.request, 'Error de conexión. Intenta más tarde.')
                return mi_error_500(request)
        
        except Exception as err:
            logger.error(f'Error inesperado: {err}')
            return mi_error_500(request)
   
    """
    def realizar_peticion2(self, metodo, url, datos=None, params=None, archivos=None, request=None):

        Método genérico para realizar peticiones HTTP para formularios,
        manejar errores y mostrar mensajes de éxito.
    
        headers = crear_cabecera()  # Obtiene el token automáticamente

        try:
            # Si se están enviando datos de formulario
            if datos:
                if isinstance(datos, dict):  # Aseguramos que los datos sean un diccionario (como un formulario)
                    data = datos
                else:
                    raise ValueError("Los datos deben ser un diccionario para enviarlos como formulario.")
            else:
                data = None

            # Dependiendo del tipo de método, realizamos la petición correspondiente
            if metodo == 'GET':
                response = requests.get(url, headers=headers, params=params)

            elif metodo == 'POST':
                response = requests.post(url, headers=headers, data=data)  # Enviar datos como formulario

            elif metodo == 'PUT':
                response = requests.put(url, headers=headers, data=data)

            elif metodo == 'PATCH':
                response = requests.patch(url, headers=headers, data=data)

            elif metodo == 'DELETE':
                response = requests.delete(url, headers=headers)

            elif metodo == 'PATCH-FILE':
                response = requests.patch(url, files=archivos)  # Si es un archivo, lo enviamos directamente

            else:
                raise ValueError("Método HTTP no soportado.")
            
            # Si la respuesta HTTP es exitosa, devolvemos la respuesta
            response.raise_for_status()  # Lanza excepción para errores HTTP
            return response

        except HTTPError as http_err:
            # Si ocurre un error HTTP, lo registramos
            if http_err.response is not None:
                try:
                    errores_json = http_err.response.json()
                    logger.error(f'Error HTTP {http_err.response.status_code}: {errores_json}')
                except ValueError:
                    logger.error(f'Error HTTP {http_err.response.status_code}: {http_err.response.text}')
            else:
                logger.error(f'Error HTTP sin respuesta: {http_err}')
            
            return http_err.response  # Retorna la respuesta con el error
        
        except (ConnectionError, Timeout) as conn_err:
            logger.error(f'Error de conexión o timeout: {conn_err}')
            if requests.request:
                messages.error(requests.request, 'Error de conexión. Intenta más tarde.')
                return mi_error_500(request)

        except Exception as err:
            logger.error(f'Error inesperado: {err}')
            return mi_error_500(request)
    """


    def procesar_respuesta(self, request, response, formulario=None, exito_msg="Operación exitosa.", redirect_url="index"):
        if response.status_code in [200, 201]:
            messages.success(request, exito_msg)
            return redirect(redirect_url)
        
        elif response.status_code == 400:
            errores = response.json()

            # Manejo de errores específicos
            if errores.get('error') == "El torneo no tiene una imagen asignada":
                messages.warning(request, "El torneo no tiene una imagen asignada.")
                return redirect(redirect_url)
            
            # Si el error es diferente, aplica el manejo genérico
            if formulario:
                for campo, mensaje in errores.items():
                    formulario.add_error(campo, mensaje)
                    
            messages.error(request, 'Error en los datos proporcionados. Revisa los campos.')
            return None
        # Manejo de errores 404, 500 y otros y el logueo de los errores
        elif response.status_code == 404:
            logger.error('Error 404: Recurso no encontrado.')
            messages.error(request, 'Recurso no encontrado.')
            return mi_error_404(request)
        
        elif response.status_code == 500:
            logger.error(f'Error 500: {response.text}')
            messages.error(request, 'Ocurrió un error en el servidor. Intenta más tarde.')
            return mi_error_500(request)
        
        else:
            logger.error(f'Error desconocido: {response.status_code} - {response.text}')
            messages.error(request, 'Ocurrió un error inesperado. Intenta nuevamente.')
            return mi_error_500(request)

        
    def manejar_error_400(self, response, formulario, template_name, request):
        """
        Centraliza el manejo de errores 400 en la aplicación.
        """
        errores = process_response(response)
        for campo, mensaje in errores.items():
            formulario.add_error(campo, mensaje)
        
        return render(request, template_name, {"formulario": formulario, "errores": errores})
        
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


    