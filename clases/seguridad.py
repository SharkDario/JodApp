from django.db import models
from .empleado import Empleado

class Seguridad(Empleado):
    _entrada_asignada = models.CharField(max_length=100, verbose_name="Entrada Asignada")

    @property
    def entrada_asignada(self):
        return self._entrada_asignada

    @entrada_asignada.setter
    def entrada_asignada(self, value):
        self._entrada_asignada = value

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Seguridad)"

    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Guardia de Seguridad"
        verbose_name_plural = "Guardias de Seguridad"