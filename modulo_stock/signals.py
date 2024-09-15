from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Producto, Fabricacion, DetalleRemitoProveedor, MovimientoStock

# Señal para actualizar el stock del trago cuando se actualiza un producto
@receiver(post_save, sender=Producto)
def actualizar_stock_trago(sender, instance, **kwargs):
    # Obtiene todas las fabricaciones que usan este producto
    fabricaciones = Fabricacion.objects.filter(_producto=instance)
    
    for fabricacion in fabricaciones:
        # Actualiza el stock del trago relacionado con cada fabricación
        fabricacion.trago.actualizar_stock()

# Señal para actualizar el stock del trago cuando se elimina un producto
@receiver(post_delete, sender=Producto)
def actualizar_stock_trago_eliminar(sender, instance, **kwargs):
    # Obtiene todas las fabricaciones que usan este producto
    fabricaciones = Fabricacion.objects.filter(_producto=instance)
    
    for fabricacion in fabricaciones:
        # Actualiza el stock del trago relacionado con cada fabricación
        fabricacion.trago.actualizar_stock()

@receiver(post_save, sender=DetalleRemitoProveedor)
def actualizar_stock_producto(sender, instance, created, **kwargs):
    if created:
        producto = instance.producto
        producto.stock += instance.cantidad
        producto.save()

@receiver(post_save, sender=Producto)
def registrar_movimiento_stock(sender, instance, **kwargs):
    # Obtener el cambio de stock
    try:
        producto_anterior = sender.objects.get(pk=instance.pk)
        cambio_stock = instance._stock - producto_anterior._stock
    except sender.DoesNotExist:
        # Si el producto no existe, es una nueva creación (no registrar movimiento)
        return

    # Si no hubo cambio de stock, no registrar nada
    if cambio_stock == 0:
        return

    # Obtener el empleado relacionado con el usuario que hizo la modificación (esto depende de cómo registres al usuario en admin)
    # Si usas `request.user` en admin, este debe estar relacionado con un empleado.
    usuario = instance._empleado  # Suponiendo que tienes acceso al empleado que realiza el cambio

    # Registrar el movimiento de stock
    MovimientoStock.objects.create(
        _empleado=usuario,
        _producto=instance,
        _cantidad=cambio_stock,
        _fecha_movimiento=timezone.now()
    )