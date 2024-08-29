from django.db import models
from django.utils import timezone

class Contratacion(models.Model):
    administrador = models.ForeignKey('Administrador', on_delete=models.CASCADE, related_name='contrataciones_administradas')
    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE, related_name='contrataciones')
    fecha_contratacion = models.DateField(default=timezone.now)

    def finalizar_contrato(self):
        pass

    def renovar_contrato(self):
        pass

    def __str__(self):
        return f"{self.administrador} contrató a {self.empleado} el {self.fecha_contratacion}"
    
    class Meta:
        app_label = 'moduloLogin'

"""
from django.db import models
from django.utils import timezone
from .empleado import Empleado
from .administrador import Administrador

class Contratacion(models.Model):
    administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, related_name='contrataciones_administradas')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, related_name='contrataciones')
    fecha_contratacion = models.DateField(default=timezone.now)

    def finalizar_contrato(self):
        pass

    def renovar_contrato(self):
        pass

    def __str__(self):
        return f"{self.administrador} contrató a {self.empleado} el {self.fecha_contratacion}"
"""