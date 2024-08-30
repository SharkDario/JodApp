from django.db import models
from .empleado import Empleado

class Cajero(Empleado):
    _caja_asignada = models.CharField(max_length=100)

    @property
    def caja_asignada(self):
        return self._caja_asignada

    @caja_asignada.setter
    def caja_asignada(self, value):
        self._caja_asignada = value

    class Meta:
        app_label = 'moduloLogin'

"""
from django.db import models
from .empleado import Empleado

class Cajero(Empleado):
    caja_asignada = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'moduloLogin'
"""