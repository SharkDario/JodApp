from django.db import models

class TipoFactura(models.Model):
    _descripcion = models.CharField(verbose_name="Descripción", max_length=100)

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, value):
        self._descripcion = value

    def __str__(self):
        return f"{self.descripcion}"

    class Meta:
        app_label = 'modulo_ventas'
        verbose_name = "Tipo Factura"
        verbose_name_plural = "Tipos Factura"
