import json
from django.shortcuts import redirect, render
import requests
import environ
import os
import xml.etree.ElementTree as ET
import logging
from django.contrib import messages
from requests.exceptions import HTTPError
logger = logging.getLogger(__name__)


def crear_cabecera():
    helper = Helper()
    
    # Si ya tenemos el token, lo usamos
    if helper.token:
        return {
            'Authorization': f'Bearer {helper.token}',
            'Content-Type': 'application/json'
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
        'Content-Type': 'application/json'
    }



env = environ.Env()

# Construye el path de BASE_DIR (en settings.py ya está definido, pero si no, agrégalo)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carga las variables del archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

API_VERSION = env("API_VERSION", default="v1") 
API_BASE_URL = f'http://127.0.0.1:8000/api/{API_VERSION}/'
API_BASE_TOKEN = f'http://127.0.0.1:8000/'

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
    
    def realizar_peticion(self, metodo, url, datos=None, archivos=None, request=None):
        """
        Método genérico para realizar peticiones HTTP, manejar errores y mostrar mensajes de éxito.
        """
        headers = crear_cabecera()
        try:
            if metodo == 'GET':
                response = requests.get(url, headers=headers)
            elif metodo == 'POST':
                response = requests.post(url, headers=headers, data=json.dumps(datos))
            elif metodo == 'PUT':
                response = requests.put(url, headers=headers, data=json.dumps(datos))
            elif metodo == 'PATCH':
                response = requests.patch(url, headers=headers, data=json.dumps(datos))
            elif metodo == 'DELETE':
                response = requests.delete(url, headers=headers)
            elif metodo == 'PATCH-FILE':
                response = requests.patch(url, headers=headers, files=archivos)
            else:
                raise ValueError("Método HTTP no soportado.")
            
            response.raise_for_status()  # Lanza excepción para errores HTTP
            return response
        
        except HTTPError as http_err:
            # 👉 Ahora mostramos el detalle de la respuesta
            if http_err.response is not None:
                try:
                    errores_json = http_err.response.json()
                    logger.error(f'Error HTTP {http_err.response.status_code}: {errores_json}')
                except ValueError:
                    logger.error(f'Error HTTP {http_err.response.status_code}: {http_err.response.text}')
            else:
                logger.error(f'Error HTTP sin respuesta: {http_err}')
            
            # ✅ Devolvemos la respuesta para que `procesar_respuesta()` lo maneje
            return http_err.response
        
        except (ConnectionError, requests.Timeout) as conn_err:
            # ✅ Ahora manejamos `ConnectionError` y `Timeout` correctamente
            logger.error(f'Error de conexión o timeout: {conn_err}')
            if requests.request:
                messages.error(requests.request, 'Error de conexión. Intenta más tarde.')
                # 👉 Redirige automáticamente a `mi_error_500`
                return redirect('mi_error_500')
        
        except Exception as err:
            logger.error(f'Error inesperado: {err}')
            return redirect('mi_error_500')

    def procesar_respuesta(self, request, response, formulario=None, exito_msg="Operación exitosa.", redirect_url="index"):
        """
        Procesa la respuesta y maneja errores.
        """
        if response.status_code in [200, 201]:
            messages.success(request, exito_msg)
            return redirect(redirect_url)
        
        elif response.status_code == 400:
            errores = response.json()
            if formulario:
                for campo, mensaje in errores.items():
                    formulario.add_error(campo, mensaje)
            messages.error(request, 'Error en los datos proporcionados. Revisa los campos.')
            return None
        
        elif response.status_code == 404:
            logger.error('Error 404: Recurso no encontrado.')
            messages.error(request, 'Recurso no encontrado.')
            return redirect('mi_error_404')
        
        elif response.status_code == 500:
            logger.error(f'Error 500: {response.text}')
            messages.error(request, 'Ocurrió un error en el servidor. Intenta más tarde.')
            return redirect('mi_error_500')
        
        else:
            logger.error(f'Error desconocido: {response.status_code} - {response.text}')
            messages.error(request, 'Ocurrió un error inesperado. Intenta nuevamente.')
            return redirect('mi_error_500')
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