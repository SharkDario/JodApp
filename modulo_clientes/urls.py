from django.urls import path
from .views import registrar_cliente

urlpatterns = [
    path('registrar/', registrar_cliente, name='registrar'),
]
