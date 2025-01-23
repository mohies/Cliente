from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listar-torneos/', views.torneos_lista_api, name='listar_torneos'),
]
