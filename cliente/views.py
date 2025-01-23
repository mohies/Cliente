from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    return render(request, 'index.html')


def torneos_lista_api(request):
    # Obtenemos todos los torneos desde la API
    headers= {'Authorization': 'Bearer lu3yXke3GuRaJSNcK4LfZD1khxe0nx'}
    response = requests.get('http://127.0.0.1:8000/api/v1/torneos/', headers=headers)  # Cambia la URL si es necesario
    
    # Transformamos la respuesta en JSON
    torneos = response.json()
    
    # Renderizamos los datos en la plantilla HTML
    return render(request, 'cliente/lista_api.html', {"torneos_mostrar": torneos})
