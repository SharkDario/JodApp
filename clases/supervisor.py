from django.db import models
from .empleado import Empleado

class Supervisor(Empleado):
    frecuencia = models.PositiveIntegerField()

    class Meta:
        app_label = 'moduloLogin'
