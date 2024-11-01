from django.db import models
from django.core.validators import MinValueValidator
from .fiesta import Fiesta

class EntradaManager(models.Manager):
    def get_queryset(self):
        # Sobrescribir el queryset para que use los nombres de campo con guion bajo
        return super().get_queryset()

    def filter_by_fiesta(self, fiesta):
        # Permite filtrar por _dni utilizando el manager personalizado
        return self.get_queryset().filter(_fiesta=fiesta)

class Entrada(models.Model):
    CATEGORIA_CHOICES = [
        ('Popular', 'Popular'),
        ('VIP', 'VIP'),
    ]
    _fiesta = models.ForeignKey(Fiesta, on_delete=models.CASCADE, verbose_name="Fiesta")
    _categoria = models.CharField(verbose_name="Categoría", max_length=20, choices=CATEGORIA_CHOICES)
    _precio_unitario = models.DecimalField(verbose_name="Precio Unitario", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)

    objects = EntradaManager()  # Usar el manager personalizado

    @property
    def precio_unitario(self):
        return self._precio_unitario
    
    @precio_unitario.setter
    def precio_unitario(self, value):
        self._precio_unitario = value

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
        return f"Entrada [{self.categoria}] [{self.fiesta}]"

    class Meta:
        app_label = 'modulo_evento'
        verbose_name = "Entrada"
        verbose_name_plural = "Entradas"