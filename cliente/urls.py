from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
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
 
    path('registro/', views.registrar_usuario, name='registrar_usuario'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'), #url en la cual nos lleva al reseto para llevarnos a la pagina a llevar un correo para restablecerla contraseña
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),#url confirmacion de contraseña
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    
    path('torneos/mis-torneos/', views.torneos_usuario_view, name="torneos_usuario_view"),
    path('mis-torneos-jugadores/', views.torneos_usuario_con_jugadores_view, name="torneos-usuario-jugadores"),

    path("test-cors/", views.test_cors_view, name="test-cors"),
    


]
