from django.urls import path
from . import views  # Importar las vistas de la aplicación

urlpatterns = [
    path('mapa-mesas/', views.mapa_mesas_view, name='mapa_mesas'),
]
