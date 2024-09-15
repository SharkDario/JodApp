from django.db import models
from .empleado import Empleado
from .producto import Producto

class MovimientoStock(models.Model):
    _empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Empleado")
    _producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name="Producto")
    _cantidad = models.IntegerField(verbose_name="Cantidad (+-)")
    _fecha_movimiento = models.DateField(verbose_name="Fecha de movimiento")

    @property
    def empleado(self):
        return self._empleado

    @property
    def producto(self):
        return self._producto

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def fecha_movimiento(self):
        return self._fecha_movimiento

    @cantidad.setter
    def cantidad(self, value):
        self._cantidad = value

    @fecha_movimiento.setter
    def fecha_movimiento(self, value):
        self._fecha_movimiento = value

    def __str__(self):
        return f"{self.empleado} - {self.producto} - {self.cantidad} - {self.fecha_movimiento}"

    class Meta:
        app_label = 'modulo_stock'
        verbose_name = "Movimiento de stock"
        verbose_name_plural = "Movimientos de stock"
