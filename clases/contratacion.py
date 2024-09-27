from django.db import models
from django.utils import timezone

class Contratacion(models.Model):
    _tipo = models.CharField(max_length=50, choices=[('Contratacion', 'Contratacion'), ('Renovacion', 'Renovacion'), ('Despido', 'Despido')], verbose_name="Tipo")
    _administrador = models.ForeignKey('Administrador', on_delete=models.CASCADE, related_name='contrataciones_administradas', verbose_name="Administrador")
    _empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE, related_name='contrataciones', verbose_name="Empleado")
    _fecha_contratacion = models.DateField(verbose_name="Fecha Contratación", default=timezone.now)
    
    @property
    def tipo(self):
        return self._tipo

    @property
    def administrador(self):
        return self._administrador

    @property
    def empleado(self):
        return self._empleado

    @property
    def fecha_contratacion(self):
        return self._fecha_contratacion

    def finalizar_contrato(self):
        self.empleado.estado = 'Inactivo'
        self.empleado.save()

    def renovar_contrato(self):
        self.empleado.estado = 'Activo'
        self.empleado.save()

    def save(self, *args, **kwargs):
        # Si el tipo es "Despido", ejecutar la lógica de finalizar contrato
        if self.tipo == 'Despido':
            self.finalizar_contrato()
        else:
            self.renovar_contrato()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.administrador} contrató a {self.empleado} el {self.fecha_contratacion}"
    
    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Contratación"
        verbose_name_plural = "Gestión de contrataciones"

