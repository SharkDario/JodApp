from django.db import models
from .proveedor import Proveedor
from .empleado import Empleado

class RemitoProveedor(models.Model):
    _proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name="Proveedor")
    _empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Empleado", default=None)
    _fecha_emision_remito = models.DateField(verbose_name="Fecha de emisión")
    _numero_remito = models.CharField(max_length=100, verbose_name="Número")

    @property
    def proveedor(self):
        return self._proveedor

    @property
    def empleado(self):
        return self._empleado

    @property
    def fecha_emision_remito(self):
        return self._fecha_emision_remito

    @property
    def numero_remito(self):
        return self._numero_remito

    @fecha_emision_remito.setter
    def fecha_emision_remito(self, value):
        self._fecha_emision_remito = value

    @numero_remito.setter
    def numero_remito(self, value):
        self._numero_remito = value

    def __str__(self):
        return f"Proveedor:{self.proveedor} - N°:{self.numero_remito} - Fecha:{self.fecha_emision_remito}"

    class Meta:
        app_label = 'modulo_stock'
        unique_together = (('_proveedor', '_numero_remito'),)
        verbose_name = "Remito (Proveedor)"
        verbose_name_plural = "Remitos (Proveedor)"
