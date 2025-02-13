import requests
import environ
import os

def crear_cabecera():
    return {
        'Authorization': 'Bearer MMa4V7TzIMdRgUZ09iGKFmnlosO4IG',
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


