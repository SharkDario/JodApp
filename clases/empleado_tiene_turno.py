from django.db import models
from clases.empleado import Empleado
from clases.turno import Turno

class EmpleadoTieneTurno(models.Model):
    _empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Empleado")
    _turno = models.ForeignKey(Turno, on_delete=models.CASCADE, verbose_name="Turno")

    @property
    def empleado(self):
        return self._empleado

    @property
    def turno(self):
        return self._turno

    def __str__(self):
        return f"{self.empleado} tiene el turno {self.turno}"

    class Meta:
        app_label = 'moduloLogin'
        verbose_name = 'Asignación de Turno'

"""
from django.db import models
from clases.empleado import Empleado
from clases.turno import Turno

class EmpleadoTieneTurno(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)

    class Meta:
        app_label = 'moduloLogin'
"""