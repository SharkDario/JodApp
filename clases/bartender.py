from django.db import models
from .empleado import Empleado

class Bartender(Empleado):
    barra_asignada = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'moduloLogin'
