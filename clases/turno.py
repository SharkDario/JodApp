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
