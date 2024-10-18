from django.db import models
from .detalle_factura import DetalleFactura
from .articulo import Articulo

class DetalleArticulo(DetalleFactura):
    _articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, verbose_name="Bebida")

    @property
    def articulo(self):
        return self._articulo

    @articulo.setter
    def articulo(self, value):
        self._articulo = value

    def save(self, *args, **kwargs):
        # Extraer el precio del artículo relacionado
        """if self._articulo:
            self._precio_unitario = self._articulo.precio_unitario"""
        
        # Calcular el subtotal (cantidad * precio unitario)
        self._subtotal = self._cantidad * self._precio_unitario

        # Llamar al método save original para guardar los cambios
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'modulo_ventas'
        verbose_name = "Detalle de Bebida"
        verbose_name_plural = "Detalles de Bebida"
