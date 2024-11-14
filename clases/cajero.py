from django.db import models
from .empleado import Empleado
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType

class Cajero(Empleado):
    _caja_asignada = models.CharField(verbose_name="Caja Asignada", max_length=100)

    @property
    def caja_asignada(self):
        return self._caja_asignada

    @caja_asignada.setter
    def caja_asignada(self, value):
        self._caja_asignada = value

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Cajero)"

    def save(self, *args, **kwargs):
        if self._user:
            content_types = ContentType.objects.filter(app_label='modulo_ventas')
            ventas_permissions = Permission.objects.filter(content_type__in=content_types)
            for perm in ventas_permissions:
                self._user.user_permissions.add(perm)

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

        super().save(*args, **kwargs)

    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Cajero"
        verbose_name_plural = "Cajeros"