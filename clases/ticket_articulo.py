from django.db import models
from .articulo import Articulo
from .cliente import Cliente
from .producto import Producto

class TicketArticuloManager(models.Manager):
    def get_queryset(self):
        # Sobrescribir el queryset para que use los nombres de campo con guion bajo
        return super().get_queryset()

class TicketArticulo(models.Model):
    _cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente")
    _articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, verbose_name="Bebida")
    _cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    _fecha_limite = models.DateTimeField(verbose_name="Fecha Límite", auto_now_add=True)

    objects = TicketArticuloManager()  # Usar el manager personalizado

    @property
    def cliente(self):
        return self._cliente

    @property
    def articulo(self):
        return self._articulo

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def fecha_limite(self):
        return self._fecha_limite

    @cliente.setter
    def cliente(self, value):
        self._cliente = value

    @articulo.setter
    def articulo(self, value):
        self._articulo = value

    @cantidad.setter
    def cantidad(self, value):
        self._cantidad = value

    @fecha_limite.setter
    def fecha_limite(self, value):
        self._fecha_limite = value

    def __str__(self):
        return f"{self.cliente} tiene {self.cantidad} bebidas ({self.articulo}) para canjear"
    
    def save(self, *args, **kwargs):
        if self.pk:
            # Si existe, obtenemos la instancia anterior
            previous_instance = TicketArticulo.objects.get(pk=self.pk)
            cantidad_diferencia = self.cantidad - previous_instance.cantidad
        else:
            cantidad_diferencia = self.cantidad

        super().save(*args, **kwargs)  # Guardar la instancia actual

        # Solo ajustar el stock si el artículo es un Producto
        if isinstance(self.articulo, Producto):  # Verificar si el artículo es un Producto
            if self._articulo.stock - cantidad_diferencia < 0:
                raise ValueError("No hay suficiente stock para este producto.")
            self._articulo.stock -= cantidad_diferencia
            self._articulo.save()
    
    class Meta:
        app_label = 'modulo_clientes'
        verbose_name = "Ticket Bebida"
        verbose_name_plural = "Tickets Bebidas"