from django.db import models
from .empleado import Empleado

class Auditor(Empleado):
    _frecuencia = models.PositiveIntegerField()

    @property
    def frecuencia(self):
        return self._frecuencia

    @frecuencia.setter
    def frecuencia(self, value):
        self._frecuencia = value

    class Meta:
        app_label = 'moduloLogin'

"""
from django.db import models
from .empleado import Empleado

class Auditor(Empleado):
    frecuencia = models.PositiveIntegerField()
    
    class Meta:
        app_label = 'moduloLogin'
"""
