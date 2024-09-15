from django.db import models

class Turno(models.Model):
    _hora_inicio = models.TimeField(verbose_name="Hora Inicio")
    _hora_fin = models.TimeField(verbose_name="Hora Fin")

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

    def __str__(self):
        return f"(Hora inicio: {self.hora_inicio}. Hora fin: {self.hora_fin}.)"

    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"
