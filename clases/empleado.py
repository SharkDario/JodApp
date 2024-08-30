from django.db import models
from .persona import Persona

class Empleado(Persona):
    _zona_asignada = models.CharField(max_length=100, choices=[('Planta baja', 'Planta baja'), ('Primer piso', 'Primer piso')])
    _sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    _estado = models.CharField(max_length=50, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])
    _telefono = models.CharField(max_length=50)
    _fecha_inicio = models.DateField()
    _seniority = models.CharField(max_length=50, choices=[('Trainee', 'Trainee'), ('Junior', 'Junior'), ('Senior', 'Senior')])
    _annos_experiencia = models.PositiveIntegerField()

    @property
    def zona_asignada(self):
        return self._zona_asignada

    @zona_asignada.setter
    def zona_asignada(self, value):
        self._zona_asignada = value

    @property
    def sueldo(self):
        return self._sueldo

    @sueldo.setter
    def sueldo(self, value):
        self._sueldo = value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, value):
        self._telefono = value

    @property
    def fecha_inicio(self):
        return self._fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, value):
        self._fecha_inicio = value

    @property
    def seniority(self):
        return self._seniority

    @seniority.setter
    def seniority(self, value):
        self._seniority = value

    @property
    def annos_experiencia(self):
        return self._annos_experiencia

    @annos_experiencia.setter
    def annos_experiencia(self, value):
        self._annos_experiencia = value

    def asignar_turno(self, turno):
        pass

    def calcular_estado(self):
        pass

    def calcular_sueldo(self):
        pass

    class Meta:
        app_label = 'moduloLogin'

"""
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
"""