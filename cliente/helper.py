import json
import requests
import environ
import os
import xml.etree.ElementTree as ET

def crear_cabecera():
    return {
        'Authorization': 'Bearer PUHJyMz5miDrM6vYCQK6gd7LQxeuMf',
        'Content-Type': 'application/json'
    }

env = environ.Env()

# Construye el path de BASE_DIR (en settings.py ya está definido, pero si no, agrégalo)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Carga las variables del archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

API_VERSION = env("API_VERSION", default="v1") 
API_BASE_URL = f'http://127.0.0.1:8000/api/{API_VERSION}/'

class Helper:
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

    def obtener_torneos(self):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}torneos/mejorada/', headers=headers)
        return self.process_response(response)

    def obtener_participantes(self):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}participantes/mejorada/', headers=headers)
        return self.process_response(response)

    def obtener_juegos(self):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}juegos/mejorada/', headers=headers)
        return self.process_response(response)

    def obtener_equipos(self):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}equipos/', headers=headers)
        return self.process_response(response)

    def buscar_torneos(self, texto_busqueda):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}torneos/buscar/', headers=headers, params={'textoBusqueda': texto_busqueda})
        return self.process_response(response)

    def buscar_torneos_avanzado(self, params):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}torneos/buscar/avanzado/', headers=headers, params=params)
        return self.process_response(response)

    def buscar_equipos_avanzado(self, params):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}equipos/buscar/avanzado/', headers=headers, params=params)
        return self.process_response(response)

    def buscar_participantes_avanzado(self, params):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}participantes/buscar/avanzado/', headers=headers, params=params)
        return self.process_response(response)

    def buscar_juegos_avanzado(self, params):
        headers = crear_cabecera()
        response = requests.get(f'{API_BASE_URL}juegos/buscar/avanzado/', headers=headers, params=params)
        return self.process_response(response)

    def crear_torneo(self, datos):
        headers = crear_cabecera()
        response = requests.post(f'{API_BASE_URL}torneos/crear/', headers=headers, data=json.dumps(datos))
        self.check_response_status(response)

    def editar_torneo(self, torneo_id, datos):
        headers = crear_cabecera()
        response = requests.put(f'{API_BASE_URL}torneos/editar/{torneo_id}/', headers=headers, data=json.dumps(datos))
        self.check_response_status(response)

    def actualizar_nombre_torneo(self, torneo_id, datos):
        headers = crear_cabecera()
        response = requests.patch(f'{API_BASE_URL}torneos/actualizar-nombre/{torneo_id}/', headers=headers, data=json.dumps(datos))
        self.check_response_status(response)

    def eliminar_torneo(self, torneo_id):
        headers = crear_cabecera()
        response = requests.delete(f'{API_BASE_URL}torneos/eliminar/{torneo_id}/', headers=headers)
        self.check_response_status(response)

    def crear_juego(self, datos):
        headers = crear_cabecera()
        response = requests.post(f'{API_BASE_URL}juegos/crear/', headers=headers, data=json.dumps(datos))
        self.check_response_status(response)

    def editar_juego(self, juego_id, datos):
        headers = crear_cabecera()
        response = requests.put(f'{API_BASE_URL}juegos/editar/{juego_id}/', headers=headers, data=json.dumps(datos))
        self.check_response_status(response)

    def actualizar_nombre_juego(self, juego_id, datos):
        headers = crear_cabecera()
        response = requests.patch(f'{API_BASE_URL}juegos/actualizar-nombre/{juego_id}/', headers=headers, data=json.dumps(datos))
        self.check_response_status(response)

    def eliminar_juego(self, juego_id):
        headers = crear_cabecera()
        response = requests.delete(f'{API_BASE_URL}juegos/eliminar/{juego_id}/', headers=headers)
        self.check_response_status(response)

    def crear_participante(self, datos):
        headers = crear_cabecera()
        response = requests.post(f'{API_BASE_URL}participantes/crear/', headers=headers, data=json.dumps(datos))
        self.check_response_status(response)

    def editar_participante(self, participante_id, datos):
        headers = crear_cabecera()
        response = requests.put(f'{API_BASE_URL}participantes/editar/{participante_id}/', headers=headers, data=json.dumps(datos))
        self.check_response_status(response)

    def actualizar_equipos_participante(self, participante_id, datos):
        headers = crear_cabecera()
        response = requests.patch(f'{API_BASE_URL}participantes/actualizar-equipos/{participante_id}/', headers=headers, data=json.dumps(datos))
        self.check_response_status(response)

    def eliminar_participante(self, participante_id):
        headers = crear_cabecera()
        response = requests.delete(f'{API_BASE_URL}participantes/eliminar/{participante_id}/', headers=headers)
        self.check_response_status(response)

    def crear_jugador(self, datos):
        headers = crear_cabecera()
        response = requests.post(f'{API_BASE_URL}jugadores/crear/', headers=headers, data=json.dumps(datos))
        self.check_response_status(response)

    def editar_jugador(self, jugador_id, datos):
        headers = crear_cabecera()
        response = requests.put(f'{API_BASE_URL}jugadores/editar/{jugador_id}/', headers=headers, data=json.dumps(datos))
        self.check_response_status(response)

    def actualizar_puntos_jugador(self, jugador_id, datos):
        headers = crear_cabecera()
        response = requests.patch(f'{API_BASE_URL}jugadores/actualizar_puntos/{jugador_id}/', headers=headers, data=json.dumps(datos))
        self.check_response_status(response)

    def eliminar_relacion_jugador_torneo(self, jugador_id, torneo_id):
        headers = crear_cabecera()
        response = requests.delete(f'{API_BASE_URL}jugadores/eliminar/{jugador_id}/{torneo_id}/', headers=headers)
        self.check_response_status(response)

    def process_response(self, response):
        if response.headers['Content-Type'] == 'application/json':
            return response.json()
        elif response.headers['Content-Type'] == 'application/xml':
            return ET.fromstring(response.content)
        else:
            raise ValueError('Unsupported content type: {}'.format(response.headers['Content-Type']))

    def check_response_status(self, response):
        if response.status_code not in [200, 201, 204]:
            if response.status_code == 400:
                raise ValueError(f"Bad Request: {response.json()}")
            response.raise_for_status()