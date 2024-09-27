from django.db import models
from django.core.validators import MinValueValidator
from .cliente import Cliente
from .fiesta import Fiesta

class Entrada(models.Model):
    CATEGORIA_CHOICES = [
        ('Popular', 'Popular'),
        ('VIP', 'VIP'),
    ]
    _cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente", null=True, blank=True)
    _fiesta = models.ForeignKey(Fiesta, on_delete=models.CASCADE, verbose_name="Fiesta")
    _categoria = models.CharField(verbose_name="Categoría", max_length=20, choices=CATEGORIA_CHOICES)
    _precio_unitario = models.DecimalField(verbose_name="Precio Unitario", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)

    @property
    def precio_unitario(self):
        return self._precio_unitario
    
    @precio_unitario.setter
    def precio_unitario(self, value):
        self._precio_unitario = value

    @property
    def cliente(self):
        return self._cliente
    
    @cliente.setter
    def cliente(self,value):
        self._cliente = value

    @property
    def fiesta(self):
        return self._fiesta
    
    @fiesta.setter
    def fiesta(self,value):
        self._fiesta = value

    @property
    def categoria(self):
        return self._categoria
    
    @categoria.setter
    def categoria(self,value):
        self._categoria = value

    def __str__(self):
        return f"Entrada ({self.categoria})"

    class Meta:
        app_label = 'modulo_evento'
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"