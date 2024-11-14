from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import transaction
from .cliente import Cliente
from .empleado import Empleado
from .tipo_factura import TipoFactura
from .medio_de_pago import MedioDePago

class FacturaManager(models.Manager):
    def get_queryset(self):
        # Sobrescribir el queryset para que use los nombres de campo con guion bajo
        return super().get_queryset()
    
    def get_latest_factura_numero_for_null_empleado(self):
        # Usar select_for_update para bloquear el acceso concurrente
        with transaction.atomic():
            latest_factura = self.filter(_empleado__isnull=True).select_for_update().order_by('-_numero_factura').first()
            return int(latest_factura.numero_factura) if latest_factura else 0
        # Toma el ultimo `_numero_factura` para `FacturaCliente` objetos donde `_empleado` es null.
        # si ninguna factura existe, retorna `0` asi pueda incrementar desde `1`.
        #latest_factura = self.filter(_empleado__isnull=True).order_by('-_numero_factura').first()
        #return int(latest_factura.numero_factura) if latest_factura else 0
    
    def get_facturas_by_cliente(self, cliente_id):
        """
        Retorna todas las facturas asociadas a un cliente específico
        """
        return self.filter(_cliente_id=cliente_id)

class FacturaCliente(models.Model):
    _cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente", null=True, blank=True)
    _empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE, verbose_name="Empleado", null=True, blank=True)
    _medio_de_pago = models.ForeignKey(MedioDePago, on_delete=models.CASCADE, verbose_name="Medio de pago")
    _numero_factura = models.CharField(verbose_name="Número de Factura", max_length=100)
    _fecha_emision = models.DateTimeField(verbose_name="Fecha de Emisión", auto_now_add=True)
    _tipo_factura = models.ForeignKey(TipoFactura, on_delete=models.CASCADE, verbose_name="Tipo Factura")
    _precio_total = models.DecimalField(verbose_name="Precio Total", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=Decimal(0))
    _pagado = models.BooleanField(verbose_name="Estado del pago", default=False)

    objects = FacturaManager()  # Usar el manager personalizado

    @property
    def cliente(self):
        return self._cliente

    @property
    def empleado(self):
        return self._empleado

    @property
    def medio_de_pago(self):
        return self._medio_de_pago

    @property
    def numero_factura(self):
        return self._numero_factura

    @property
    def fecha_emision(self):
        return self._fecha_emision

    @property
    def tipo_factura(self):
        return self._tipo_factura

    @property
    def precio_total(self):
        return self._precio_total
    
    @property
    def pagado(self):
        return self._pagado

    @cliente.setter
    def cliente(self, value):
        self._cliente = value

    @empleado.setter
    def empleado(self, value):
        self._empleado = value

    @medio_de_pago.setter
    def medio_de_pago(self, value):
        self._medio_de_pago = value

    @numero_factura.setter
    def numero_factura(self, value):
        self._numero_factura = value

    @fecha_emision.setter
    def fecha_emision(self, value):
        self._fecha_emision = value

    @tipo_factura.setter
    def tipo_factura(self, value):
        self._tipo_factura = value

    @precio_total.setter
    def precio_total(self, value):
        self._precio_total = value

    @pagado.setter
    def pagado(self, value):
        self._pagado = value

    def save(self, *args, **kwargs): 
        if not (self._cliente or self._empleado): 
            raise ValidationError("Debe haber al menos un Cliente o Empleado asociado a la factura.") 

        # Generate a new `numero_factura` if it's a new factura with no assigned `empleado`
        if self._empleado is None and not self.pk:  # Only for new instances where `_empleado` is null
            with transaction.atomic():
                # Bloquea las filas relacionadas para evitar condiciones de carrera
                latest_factura = (
                    FacturaCliente.objects.select_for_update()
                    .filter(_empleado__isnull=True)
                    .order_by('-pk')
                    .first()
                )
                # Incrementa a partir del último `_numero_factura` encontrado
                self._numero_factura = str(int(latest_factura.numero_factura) + 1) if latest_factura else "1"
                #latest_numero = FacturaCliente.objects.get_latest_factura_numero_for_null_empleado()
                #self._numero_factura = str(latest_numero + 1)  # Increment and set the new number
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Factura {self.tipo_factura} N°{self.numero_factura} ({self.fecha_emision})"

    class Meta:
        app_label = 'modulo_ventas'
        unique_together = (('_empleado', '_numero_factura'),)
        verbose_name = "Factura (Cliente)"
        verbose_name_plural = "Facturas (Cliente)"
