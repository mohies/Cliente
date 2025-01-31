from django.shortcuts import render
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
def index(request):
    return render(request, 'index.html')


def torneos_lista_api(request):
    # Obtenemos todos los torneos desde la API
    headers = {'Authorization': f'Bearer {USER_KEY_ADMINISTRADOR}'}
    response = requests.get('https://mohbenbou.pythonanywhere.com/api/v1/torneos/mejorada/', headers=headers)  # Cambia la URL si es necesario
    
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




