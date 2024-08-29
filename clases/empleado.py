from django.db import models
from .persona import Persona

class Empleado(Persona):
    ZONA_CHOICES = [
        ('Planta baja', 'Planta baja'),
        ('Primer piso', 'Primer piso'),
    ]
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    SENIORITY_CHOICES = [
        ('Trainee', 'Trainee'),
        ('Junior', 'Junior'),
        ('Senior', 'Senior'),
    ]

    zona_asignada = models.CharField(max_length=100, choices=ZONA_CHOICES)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    telefono = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    seniority = models.CharField(max_length=50, choices=SENIORITY_CHOICES)
    annos_experiencia = models.PositiveIntegerField()

    def asignar_turno(self, turno):
        pass

    def calcular_estado(self):
        pass

    def calcular_sueldo(self):
        pass

    class Meta:
        app_label = 'moduloLogin'
