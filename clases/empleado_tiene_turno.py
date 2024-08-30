from django.db import models
from clases.empleado import Empleado
from clases.turno import Turno

class EmpleadoTieneTurno(models.Model):
    _empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    _turno = models.ForeignKey(Turno, on_delete=models.CASCADE)

    @property
    def empleado(self):
        return self._empleado

    @property
    def turno(self):
        return self._turno

    class Meta:
        app_label = 'moduloLogin'

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