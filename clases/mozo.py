from django.db import models
from .empleado import Empleado
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

class Mozo(Empleado):

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Mozo)"
    
    def save(self, *args, **kwargs):
        if self._user:

            content_types = ContentType.objects.filter(app_label='modulo_stock')
            stock_permissions = Permission.objects.filter(content_type__in=content_types, codename__startswith='view_')
            for perm in stock_permissions:
                self._user.user_permissions.add(perm)
            
            stock_permissions = Permission.objects.filter(content_type__in=content_types, codename__startswith='change_')
            for perm in stock_permissions:
                self._user.user_permissions.add(perm)
                
            content_types = ContentType.objects.filter(app_label='modulo_clientes')
            clientes_permissions = Permission.objects.filter(
                content_type__in=content_types,
                codename__in=['change_ticketentrada','change_ticketarticulo', 'view_cliente', 'view_ticketentrada','view_ticketarticulo']
            )
            for perm in clientes_permissions:
                self._user.user_permissions.add(perm)
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Mozo"
        verbose_name_plural = "Mozos"
