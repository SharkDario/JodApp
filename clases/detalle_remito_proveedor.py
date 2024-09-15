from django.db import models
from .remito_proveedor import RemitoProveedor
from .producto import Producto
from .estado_producto import EstadoProducto

class DetalleRemitoProveedor(models.Model):
    _remito = models.ForeignKey(RemitoProveedor, on_delete=models.CASCADE, verbose_name="Remito")
    _producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    _estado_producto = models.ForeignKey(EstadoProducto, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Estado")
    _cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    _fecha_entrega_producto = models.DateField(verbose_name="Fecha Entrega Producto")

    @property
    def remito(self):
        return self._remito

    @property
    def producto(self):
        return self._producto

    @property
    def estado_producto(self):
        return self._estado_producto

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def fecha_entrega_producto(self):
        return self._fecha_entrega_producto

    @cantidad.setter
    def cantidad(self, value):
        self._cantidad = value

    @fecha_entrega_producto.setter
    def fecha_entrega_producto(self, value):
        self._fecha_entrega_producto = value

    def __str__(self):
        return f"{self.remito} - {self.producto} ({self.cantidad})"

    class Meta:
        app_label = 'modulo_stock'
        verbose_name = "Detalle Remito (Proveedor)"
        verbose_name_plural = "Detalles Remito (Proveedor)"
