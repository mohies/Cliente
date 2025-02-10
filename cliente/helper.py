import requests
import environ
import os

def crear_cabecera():
    return {
        'Authorization': 'Bearer KVmOJFR8XecCfMWdS0StpwVmRSb4Yt'
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

