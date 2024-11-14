from django.db import models

# Create your models here.
from clases.cliente import Cliente
from clases.persona import Persona
from clases.fiesta import Fiesta
from clases.articulo import Articulo
from clases.producto import Producto
from clases.trago import Trago
from clases.entrada import Entrada
from clases.mesa import Mesa
from clases.mesa_tiene_articulo import MesaTieneArticulo
from clases.factura_cliente import FacturaCliente
from clases.detalle_reservacion import DetalleReservacion
from clases.detalle_entrada import DetalleEntrada
from clases.detalle_articulo import DetalleArticulo
from clases.medio_de_pago import MedioDePago
from clases.tipo_factura import TipoFactura
from clases.transaccion_pago import TransaccionPago
from clases.ticket_articulo import TicketArticulo
from clases.ticket_entrada import TicketEntrada

class RachaClientes(models.Model):
    """
    Modelo que se conecta a la vista view_cliente_racha
    """
    _cliente_id = models.IntegerField(primary_key=True, verbose_name="ID del Cliente")
    nombre_cliente = models.CharField(db_column='nombre_cliente', max_length=255, verbose_name="Nombre")
    apellido_cliente = models.CharField(db_column='apellido_cliente', max_length=255, verbose_name="Apellido")
    ultima_compra = models.DateField(db_column='ultima_compra', verbose_name="Última Compra")
    racha_actual = models.IntegerField(db_column='racha_actual', verbose_name="Racha Actual")
    racha_vigente = models.IntegerField(db_column='racha_vigente', verbose_name="Racha Vigente")

    class Meta:
        managed = False
        db_table = 'view_cliente_racha'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Racha de Clientes'