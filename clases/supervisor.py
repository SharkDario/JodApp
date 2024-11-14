from django.db import models
from .empleado import Empleado
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class Supervisor(Empleado):
    _frecuencia = models.PositiveIntegerField(verbose_name="Frecuencia", help_text="(días)")

    @property
    def frecuencia(self):
        return self._frecuencia

    @frecuencia.setter
    def frecuencia(self, value):
        self._frecuencia = value

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Supervisor)"
    
    def save(self, *args, **kwargs):
        if self._user:
            content_types = ContentType.objects.filter(app_label='modulo_stock')
            stock_permissions = Permission.objects.filter(content_type__in=content_types)
            for perm in stock_permissions:
                self._user.user_permissions.add(perm)

            content_types = ContentType.objects.filter(app_label='modulo_clientes')
            clientes_permissions = Permission.objects.filter(
                content_type__in=content_types,
                codename__in=['change_ticketentrada','change_ticketarticulo', 'view_cliente', 'view_ticketentrada','view_ticketarticulo']
            )
            for perm in clientes_permissions:
                self._user.user_permissions.add(perm)

        # Call the parent class's save method to save the object
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Supervisor"
        verbose_name_plural = "Supervisores"