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
    path('torneos/actualizar-imagen/<int:torneo_id>/', views.torneo_actualizar_imagen, name='torneo_actualizar_imagen'),
    path('torneos/eliminar-imagen/<int:torneo_id>/', views.torneo_eliminar_imagen, name='torneo_eliminar_imagen'),
    
    path('juegos/crear/', views.crear_juego, name='crear_juego'),
    path('juegos/editar/<int:juego_id>/', views.editar_juego, name='editar_juego'),
    path('juegos/actualizar-nombre/<int:juego_id>/', views.juego_editar_nombre, name='juego_editar_nombre'),
    path('juegos/eliminar/<int:juego_id>/', views.juego_eliminar, name='juego_eliminar'),
    
    path('participantes/crear/', views.crear_participante, name='crear_participante'),
    path('participantes/editar/<int:participante_id>/', views.editar_participante, name='editar_participante'),
    path('participantes/editar-equipo/<int:participante_id>/', views.participante_editar_equipos, name='participante_editar_equipos'),
    path('participantes/eliminar/<int:participante_id>/', views.participante_eliminar, name='participante_eliminar'),
    
    path('jugadores/crear/', views.crear_jugador, name='crear_jugador'),
    path('jugadores/editar/<int:jugador_id>/', views.editar_jugador, name='editar_jugador'),
    path('jugadores/editar_puntos/<int:jugador_id>/', views.editar_puntos_jugador, name="editar_puntos_jugador"),
    path('jugadores/eliminar/<int:jugador_id>/<int:torneo_id>/', views.jugador_eliminar_torneo, name="jugador_eliminar_torneo"),
 

    


]
