from django.db import models
from .empleado import Empleado

class Cajero(Empleado):
    caja_asignada = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'moduloLogin'
