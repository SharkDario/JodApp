from django.db import models
from .articulo import Articulo
from .marca import Marca

class Producto(Articulo):
    _marca = models.ForeignKey(Marca, on_delete=models.CASCADE, verbose_name="Marca")

    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, value):
        self._marca = value

    def __str__(self):
        return f"{self.nombre} ({self.marca})"

    class Meta:
        app_label = 'modulo_stock'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
