from django.db import models
from .cliente import Cliente
from .entrada import Entrada

class TicketEntradaManager(models.Manager):
    def get_queryset(self):
        # Sobrescribir el queryset para que use los nombres de campo con guion bajo
        return super().get_queryset()

class TicketEntrada(models.Model):
    _cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    _entrada = models.ForeignKey(Entrada, on_delete=models.CASCADE, verbose_name="Entrada")
    _cantidad = models.PositiveIntegerField(verbose_name="Cantidad")

    objects = TicketEntradaManager()  # Usar el manager personalizado

    @property
    def cliente(self):
        return self._cliente

    @property
    def entrada(self):
        return self._entrada

    @property
    def cantidad(self):
        return self._cantidad

    @cliente.setter
    def cliente(self, value):
        self._cliente = value

    @entrada.setter
    def entrada(self, value):
        self._entrada = value

    @cantidad.setter
    def cantidad(self, value):
        self._cantidad = value

    def __str__(self):
        return f"{self.cliente} tiene {self.cantidad} entradas ({self.entrada}) para canjear"
    
    class Meta:
        app_label = 'modulo_clientes'
        verbose_name = "Ticket Entrada"
        verbose_name_plural = "Tickets Entradas"