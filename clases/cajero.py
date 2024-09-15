from django.db import models
from .empleado import Empleado

class Cajero(Empleado):
    _caja_asignada = models.CharField(verbose_name="Caja Asignada", max_length=100)

    @property
    def caja_asignada(self):
        return self._caja_asignada

    @caja_asignada.setter
    def caja_asignada(self, value):
        self._caja_asignada = value

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Cajero)"

    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Cajero"
        verbose_name_plural = "Cajeros"
