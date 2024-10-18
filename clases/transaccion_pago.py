from django.db import models
from django.utils import timezone
from .factura_cliente import FacturaCliente

class TransaccionPago(models.Model):
    _factura = models.OneToOneField(FacturaCliente, on_delete=models.CASCADE, related_name='transaccion_pago')
    _qr_url = models.URLField(verbose_name="URL del QR", blank=True, null=True)
    _qr_image = models.BinaryField(blank=True, null=True)
    _fecha_creacion = models.DateTimeField(default=timezone.now)

    @property
    def factura(self):
        return self._factura

    @factura.setter
    def factura(self, value):
        self._factura = value

    @property
    def qr_url(self):
        return self._qr_url

    @qr_url.setter
    def qr_url(self, value):
        self._qr_url = value

    @property
    def qr_image(self):
        return self._qr_image

    @qr_image.setter
    def qr_image(self, value):
        self._qr_image = value

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @fecha_creacion.setter
    def fecha_creacion(self, value):
        self._fecha_creacion = value

    def marcar_como_pagado(self):
        #Marca la factura asociada como pagada.
        self.factura.pagado = True
        self.factura.save()

    def __str__(self):
        return f"Transacción de pago para {self.factura}"
    
    class Meta:
        app_label = 'modulo_ventas'
        verbose_name = "Transacción de Pago"
        verbose_name_plural = "Transacciones de Pago"

"""
class TransaccionPago(models.Model):
    _factura = models.ForeignKey(FacturaCliente, on_delete=models.CASCADE)
    _monto_usdt = models.DecimalField(max_digits=10, decimal_places=2)
    _estado = models.CharField(max_length=20)
    _detalles_pago = models.TextField(blank=True, null=True)
    _fecha_creacion = models.DateTimeField(auto_now_add=True)
    _fecha_actualizacion = models.DateTimeField(auto_now=True)

    @property
    def factura(self):
        return self._factura

    @factura.setter
    def factura(self, value):
        self._factura = value

    @property
    def monto_usdt(self):
        return self._monto_usdt

    @monto_usdt.setter
    def monto_usdt(self, value):
        self._monto_usdt = value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value

    @property
    def detalles_pago(self):
        return self._detalles_pago

    @detalles_pago.setter
    def detalles_pago(self, value):
        self._detalles_pago = value

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @fecha_creacion.setter
    def fecha_creacion(self, value):
        self._fecha_creacion = value

    @property
    def fecha_actualizacion(self):
        return self._fecha_actualizacion

    @fecha_actualizacion.setter
    def fecha_actualizacion(self, value):
        self._fecha_actualizacion = value

    def __str__(self):
        return f"Transacción {self.pk} - Factura {self._factura.numero_factura}"
    
    class Meta:
        app_label = 'modulo_ventas'
        verbose_name = "Transacción de Pago"
        verbose_name_plural = "Transacciones de Pago"
"""