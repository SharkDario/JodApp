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
