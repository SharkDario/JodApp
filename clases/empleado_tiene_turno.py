from django.db import models
from clases.empleado import Empleado
from clases.turno import Turno

class EmpleadoTieneTurno(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)

    class Meta:
        app_label = 'moduloLogin'
