from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listar-torneos/', views.torneos_lista_api, name='listar_torneos'),
    path('listar-equipos/', views.equipos_lista_api, name='listar_equipos'),
    path('participantes/', views.participantes_lista_api, name='participantes_lista'),
    path('juegos/', views.juegos_lista_api, name='juegos_lista'),
    
    ]
