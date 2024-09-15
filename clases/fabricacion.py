from django.db import models
from .producto import Producto
from .trago import Trago
from django.core.validators import MinValueValidator

class Fabricacion(models.Model):
    _producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    _trago = models.ForeignKey(Trago, on_delete=models.CASCADE, verbose_name="Trago")
    _cantidad_producto = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="cantidad  (mililitros)", validators=[MinValueValidator(0)])

    @property
    def producto(self):
        return self._producto

    @property
    def trago(self):
        return self._trago

    @property
    def cantidad_producto(self):
        return self._cantidad_producto

    @cantidad_producto.setter
    def cantidad_producto(self, value):
        self._cantidad_producto = value

    def __str__(self):
        return f"{self.trago} - {self.producto} ({self.cantidad_producto}ml)"

    class Meta:
        app_label = 'modulo_stock'
        verbose_name = "Ingrediente"
        verbose_name_plural = "Elaboración"

    # Sobreescribir el método save para actualizar el volumen del trago cuando se agrega o edita un ingrediente
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._trago.actualizar_volumen()

    # Sobreescribir el método delete para actualizar el volumen del trago cuando se elimina un ingrediente
    def delete(self, *args, **kwargs):
        trago = self._trago
        super().delete(*args, **kwargs)
        trago.actualizar_volumen()
