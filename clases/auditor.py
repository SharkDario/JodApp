from django.db import models
from .empleado import Empleado
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType


class Auditor(Empleado):
    _frecuencia = models.PositiveIntegerField(verbose_name="Frecuencia", help_text="(días)")

    @property
    def frecuencia(self):
        return self._frecuencia

    @frecuencia.setter
    def frecuencia(self, value):
        self._frecuencia = value

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Auditor)"
    
    def save(self, *args, **kwargs):
        # Check if the user is assigned to the specific permissions group
        if self._user:
            content_types = ContentType.objects.filter(app_label='modulo_ventas')
            ventas_permissions = Permission.objects.filter(content_type__in=content_types, codename__startswith='view_')
            for perm in ventas_permissions:
                self._user.user_permissions.add(perm)

            content_types = ContentType.objects.filter(app_label='moduloLogin')
            login_permissions = Permission.objects.filter(content_type__in=content_types, codename__startswith='view_')
            for perm in login_permissions:
                self._user.user_permissions.add(perm)

            content_types = ContentType.objects.filter(app_label='modulo_eventos')
            eventos_permissions = Permission.objects.filter(content_type__in=content_types, codename__startswith='view_')
            for perm in eventos_permissions:
                self._user.user_permissions.add(perm)

            content_types = ContentType.objects.filter(app_label='modulo_clientes')
            clientes_permissions = Permission.objects.filter(content_type__in=content_types, codename__startswith='view_')
            for perm in clientes_permissions:
                self._user.user_permissions.add(perm)

            content_types = ContentType.objects.filter(app_label='modulo_stock')
            stock_permissions = Permission.objects.filter(content_type__in=content_types, codename__startswith='view_')
            for perm in stock_permissions:
                self._user.user_permissions.add(perm)
        
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Auditor"
        verbose_name_plural = "Auditores"

"""
from django.db import models
from .empleado import Empleado

class Auditor(Empleado):
    frecuencia = models.PositiveIntegerField()
    
    class Meta:
        app_label = 'moduloLogin'
"""
