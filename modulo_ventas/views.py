from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import JsonResponse, HttpResponse
#from binance.client import Client
#from binance.exceptions import BinanceAPIException
from .models import TransaccionPago, generar_qr_mercado_pago

def ver_qr_pago(request, factura_id):
    transaccion = get_object_or_404(TransaccionPago, _factura__id=factura_id)
    
    if transaccion.qr_image:
        # Si ya existe una imagen del QR guardada, la mostramos
        return HttpResponse(transaccion.qr_image, content_type="image/png")
    else:
        # Si no existe, la generamos
        factura = transaccion.factura
        qr_url, qr_image = generar_qr_mercado_pago(factura)
        transaccion.qr_url = qr_url
        transaccion.qr_image = qr_image
        transaccion.save()
        return HttpResponse(qr_image, content_type="image/png")

"""
def mostrar_qr_binance(request, transaccion_id):
    transaccion = TransaccionPago.objects.get(id=transaccion_id)
    qr_code_url = transaccion.detalles_pago.get('qrcodeUrl', '')

    return render(request, 'admin/mostrar_qr.html', {'qr_code_url': qr_code_url})

def verificar_estado_pago(request, transaccion_id):
    try:
        transaccion = TransaccionPago.objects.get(id=transaccion_id)
        client = Client(api_key=settings.BINANCE_API_KEY, api_secret=settings.BINANCE_API_SECRET)

        # implementar la lógica para verificar si el pago se ha recibido
        # Esto podría implicar revisar los depósitos recientes en tu cuenta de Binance
        # o utilizar un webhook si Binance lo proporciona para notificaciones de pago

        # Este es un ejemplo simplificado. 
        depositos = client.get_deposit_history()
        for deposito in depositos:
            if (deposito['amount'] == float(transaccion.monto_usdt) and 
                deposito['status'] == 1):  # 1 significa completado
                transaccion.estado = 'PAGADO'
                transaccion.save()
                transaccion.factura.estado_pago = 'PAGADO'
                transaccion.factura.save()
                return JsonResponse({'status': 'SUCCESS'})

        # Si no se encontró un depósito correspondiente
        return JsonResponse({'status': 'PENDING'})

    except TransaccionPago.DoesNotExist:
        return JsonResponse({'status': 'ERROR', 'message': 'Transacción no encontrada'})
    except BinanceAPIException as e:
        return JsonResponse({'status': 'ERROR', 'message': str(e)})
    except Exception as e:
        return JsonResponse({'status': 'ERROR', 'message': str(e)})
"""