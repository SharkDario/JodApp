from django.db import models
from django.core.validators import MinValueValidator

class Articulo(models.Model):
    _nombre = models.CharField(verbose_name="Nombre", max_length=100)
    _volumen = models.DecimalField(verbose_name="Volumen", max_digits=10, decimal_places=2, help_text="Volumen en mililitros", default=0, validators=[MinValueValidator(0)])
    _precio_unitario = models.DecimalField(verbose_name="Precio Unitario", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    _stock = models.PositiveIntegerField(verbose_name="Stock", default=0)
    _stock_minimo = models.PositiveIntegerField(verbose_name="Stock Mínimo")

    @property
    def nombre(self):
        return self._nombre
    
    @property
    def volumen(self):
        return self._volumen

    @property
    def precio_unitario(self):
        return self._precio_unitario

    @property
    def stock(self):
        return self._stock
    
    @property
    def stock_minimo(self):
        return self._stock_minimo

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    @volumen.setter
    def volumen(self, value):
        self._volumen = value

    @precio_unitario.setter
    def precio_unitario(self, value):
        self._precio_unitario = value

    @stock.setter
    def stock(self, value):
        self._stock = value

    @stock_minimo.setter
    def stock_minimo(self, value):
        self._stock_minimo = value
    
    def __str__(self):
        return f"{self.nombre} ({self.volumen}ml)"

    class Meta:
        app_label = 'modulo_stock'
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
