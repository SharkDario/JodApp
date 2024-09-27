from django.db import models
from django.core.validators import MinValueValidator
from .mesa import Mesa
from .articulo import Articulo

class MesaTieneArticulo(models.Model):
    _mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, verbose_name="Mesa")
    _articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, verbose_name="Bebida")
    _cantidad = models.PositiveIntegerField(verbose_name="Cantidad", default=1)

    @property
    def articulo(self):
        return self._articulo
    
    @articulo.setter
    def articulo(self,value):
        self._articulo = value

    @property
    def mesa(self):
        return self._mesa
    
    @mesa.setter
    def mesa(self,value):
        self._mesa = value

    @property
    def cantidad(self):
        return self._cantidad
    
    @cantidad.setter
    def cantidad(self,value):
        self._cantidad = value
    
    def __str__(self):
        return f"{self.mesa} tiene {self.articulo}"

    class Meta:
        app_label = 'modulo_evento'
        verbose_name = "Gestión de Bebidas"
        verbose_name_plural = "Gestión de Bebidas"