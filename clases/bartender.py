from django.db import models
from .empleado import Empleado

class Bartender(Empleado):
    _barra_asignada = models.CharField(max_length=100)

    @property
    def barra_asignada(self):
        return self._barra_asignada

    @barra_asignada.setter
    def barra_asignada(self, value):
        self._barra_asignada = value

    class Meta:
        app_label = 'moduloLogin'

"""
from django.db import models
from .empleado import Empleado

class Bartender(Empleado):
    barra_asignada = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'moduloLogin'

"""
