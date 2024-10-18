from django.db import models
from .detalle_factura import DetalleFactura
from .mesa import Mesa

class DetalleReservacion(DetalleFactura):
    _reservacion = models.ForeignKey(Mesa, on_delete=models.CASCADE, verbose_name="Reservación")

    @property
    def reservacion(self):
        return self._reservacion

    @reservacion.setter
    def reservacion(self, value):
        self._reservacion = value

    def save(self, *args, **kwargs):
        # Extraer el precio del artículo relacionado
        """if self._reservacion:
            self._precio_unitario = self._reservacion._precio"""
        
        # Calcular el subtotal (cantidad * precio unitario)
        self._subtotal = self._cantidad * self._precio_unitario

        # Llamar al método save original para guardar los cambios
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'modulo_ventas'
        verbose_name = "Detalle de Reservación"
        verbose_name_plural = "Detalle de Reservación"
