from django.db import models

class Turno(models.Model):
    _hora_inicio = models.TimeField()
    _hora_fin = models.TimeField()

    @property
    def hora_inicio(self):
        return self._hora_inicio

    @hora_inicio.setter
    def hora_inicio(self, value):
        self._hora_inicio = value

    @property
    def hora_fin(self):
        return self._hora_fin

    @hora_fin.setter
    def hora_fin(self, value):
        self._hora_fin = value

    def cambiar_horario(self, hora_inicio, hora_fin):
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.save()

    class Meta:
        app_label = 'moduloLogin'
"""
from django.db import models

class Turno(models.Model):
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def cambiar_horario(self, hora_inicio, hora_fin):
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.save()

    class Meta:
        app_label = 'moduloLogin'
"""