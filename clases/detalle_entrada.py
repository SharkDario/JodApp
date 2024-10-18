from django.db import models
from .detalle_factura import DetalleFactura
from .entrada import Entrada

class DetalleEntrada(DetalleFactura):
    _entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE, verbose_name="Entrada")

    @property
    def entrada(self):
        return self._entrada

    @entrada.setter
    def entrada(self, value):
        self._entrada = value

    def save(self, *args, **kwargs):
        # Extraer el precio del artículo relacionado
        """if self._entrada:
            self._precio_unitario = self._entrada._precio_unitario"""
        
        # Calcular el subtotal (cantidad * precio unitario)
        self._subtotal = self._cantidad * self._precio_unitario

        # Llamar al método save original para guardar los cambios
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'modulo_ventas'
        verbose_name = "Detalle de Entrada"
        verbose_name_plural = "Detalles de Entrada"
