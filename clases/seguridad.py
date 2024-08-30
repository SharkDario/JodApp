from django.db import models
from .empleado import Empleado

class Seguridad(Empleado):
    _entrada_asignada = models.CharField(max_length=100)

    @property
    def entrada_asignada(self):
        return self._entrada_asignada

    @entrada_asignada.setter
    def entrada_asignada(self, value):
        self._entrada_asignada = value

    class Meta:
        app_label = 'moduloLogin'
"""
from django.db import models
from .empleado import Empleado

class Seguridad(Empleado):
    entrada_asignada = models.CharField(max_length=100)

    class Meta:
        app_label = 'moduloLogin'
"""