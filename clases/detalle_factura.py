from django.db import models
from django.core.validators import MinValueValidator
from .factura_cliente import FacturaCliente

class DetalleFacturaManager(models.Manager):
    def get_queryset(self):
        # Sobrescribir el queryset para que use los nombres de campo con guion bajo
        return super().get_queryset()
    
    def get_reservaciones_by_cliente(self, cliente_id):
        """
        Retorna todas las reservaciones asociadas a las facturas de un cliente
        """
        # Obtener todas las facturas del cliente
        facturas = FacturaCliente.objects.get_facturas_by_cliente(cliente_id)
        # Retornar todas las reservaciones asociadas a esas facturas
        return self.filter(_factura__in=facturas)


class DetalleFactura(models.Model):
    _factura = models.ForeignKey(FacturaCliente, on_delete=models.CASCADE, verbose_name="Factura")
    _cantidad = models.PositiveIntegerField(verbose_name="Cantidad")
    _precio_unitario = models.DecimalField(verbose_name="Precio Unitario", max_digits=10, validators=[MinValueValidator(0)], decimal_places=2)
    _subtotal = models.DecimalField(verbose_name="Subtotal", max_digits=10, validators=[MinValueValidator(0)], decimal_places=2, default=0)

    objects = DetalleFacturaManager()  # Usar el manager personalizado

    @property
    def factura(self):
        return self._factura

    @property
    def cantidad(self):
        return self._cantidad

    @property
    def precio_unitario(self):
        return self._precio_unitario

    @property
    def subtotal(self):
        return self._subtotal

    @factura.setter
    def factura(self, value):
        self._factura = value

    @cantidad.setter
    def cantidad(self, value):
        self._cantidad = value

    @precio_unitario.setter
    def precio_unitario(self, value):
        self._precio_unitario = value

    @subtotal.setter
    def subtotal(self, value):
        self._subtotal = value

    def __str__(self):
        return "Detalle"

    class Meta:
        app_label = 'modulo_ventas'
        verbose_name = "Detalle Factura (Cliente)"
        verbose_name_plural = "Detalle Factura (Cliente)"
