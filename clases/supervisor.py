from django.db import models
from .empleado import Empleado

class Supervisor(Empleado):
    _frecuencia = models.PositiveIntegerField(verbose_name="Frecuencia", help_text="(días)")

    @property
    def frecuencia(self):
        return self._frecuencia

    @frecuencia.setter
    def frecuencia(self, value):
        self._frecuencia = value

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Supervisor)"

    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Supervisor"
        verbose_name_plural = "Supervisores"