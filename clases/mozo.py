from django.db import models
from .empleado import Empleado

class Mozo(Empleado):

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Mozo)"

    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Mozo"
        verbose_name_plural = "Mozos"
