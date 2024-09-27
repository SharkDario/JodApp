from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Fiesta, MovimientoFiesta

"""@receiver(post_save, sender=Fiesta)
def create_movimientofiesta(sender, instance, created, **kwargs):
    administrador_actual =  instance._empleado
    if created:
        # Obtener la fecha y el administrador actual
        fecha_actual = timezone.now()

        # Crear el registro en MovimientoFiesta
        MovimientoFiesta.objects.create(
            _fiesta=instance,
            _administrador=administrador_actual,
            _fecha=fecha_actual,
            _descripcion="registró"
            
        )"""