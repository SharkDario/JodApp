from django.db import models
import mercadopago
import qrcode
from django.conf import settings
from io import BytesIO

def generar_qr_mercado_pago(factura):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)  # Coloca aquí tu token de acceso de Mercado Pago
    preference_data = {
        "items": [
            {
                "title": f"Factura N° {factura.numero_factura}",
                "quantity": 1,
                "unit_price": float(factura.precio_total),
            }
        ],
        "payment_methods": {
            "excluded_payment_types": [{"id": "ticket"}]
        },
        "external_reference": str(factura.id),
        "back_urls": {
            "success": "https://tudominio.com/pago/exitoso/",
            "failure": "https://tudominio.com/pago/fallido/",
            "pending": "https://tudominio.com/pago/pendiente/"
        },
        "auto_return": "approved"
    }
    preference_response = sdk.preference().create(preference_data)
    init_point = preference_response["response"]["init_point"]
    
    # Generar el código QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(init_point)
    qr.make(fit=True)
    
    # Crear una imagen del código QR
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar la imagen en un buffer de bytes
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_image = buffer.getvalue()
    
    return init_point, qr_image

from clases.detalle_reservacion import DetalleReservacion
from clases.detalle_entrada import DetalleEntrada
from clases.detalle_articulo import DetalleArticulo
from clases.medio_de_pago import MedioDePago
from clases.tipo_factura import TipoFactura
from clases.detalle_factura import DetalleFactura
from clases.factura_cliente import FacturaCliente
from clases.articulo import Articulo
from clases.transaccion_pago import TransaccionPago
from clases.mesa import Mesa