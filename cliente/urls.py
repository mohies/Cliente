from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listar-torneos/', views.torneos_lista_api, name='listar_torneos'),
    path('listar-equipos/', views.equipos_lista_api, name='listar_equipos'),
    path('participantes/', views.participantes_lista_api, name='participantes_lista'),
    path('juegos/', views.juegos_lista_api, name='juegos_lista'),
    path('torneo/busqueda/', views.torneo_busqueda_simple, name='torneo_busqueda_simple'),
    path('torneo/busqueda/avanzada/', views.torneo_busqueda_avanzada, name='torneo_buscar_avanzado_sin_validaciones'),
    path('equipo/busqueda/avanzada/', views.equipo_busqueda_avanzada, name='equipo_busqueda_avanzada'),
    path('participante/busqueda/avanzada/', views.participante_busqueda_avanzada, name='participante_busqueda_avanzada'),
    path('juego/busqueda/avanzada/', views.juego_busqueda_avanzada, name='juego_busqueda_avanzada'),
    path('crear-torneo/', views.crear_torneo, name='crear_torneo'),
    path('editar-torneo/<int:torneo_id>/', views.editar_torneo, name='editar_torneo'),
    path('torneos/actualizar-nombre/<int:torneo_id>/', views.torneo_editar_nombre, name='torneo_editar_nombre'),
    path('torneos/eliminar/<int:torneo_id>/', views.torneo_eliminar, name='torneo_eliminar'),
    path('juegos/crear/', views.crear_juego, name='crear_juego'),
    path('juegos/editar/<int:juego_id>/', views.editar_juego, name='editar_juego'),





]
