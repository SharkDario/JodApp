from django.db import models
from .empleado import Empleado
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class Seguridad(Empleado):
    _entrada_asignada = models.CharField(max_length=100, verbose_name="Entrada Asignada")

    @property
    def entrada_asignada(self):
        return self._entrada_asignada

    @entrada_asignada.setter
    def entrada_asignada(self, value):
        self._entrada_asignada = value

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Seguridad)"

    def save(self, *args, **kwargs):
        # Check if the user is assigned to the specific permissions group
        if self._user:
            content_types = ContentType.objects.filter(app_label='modulo_clientes')
            clientes_permissions = Permission.objects.filter(
                content_type__in=content_types,
                codename__in=['view_cliente','view_ticketentrada','view_ticketarticulo']
            )
            for perm in clientes_permissions:
                self._user.user_permissions.add(perm)

        # Call the parent class's save method to save the object
        super().save(*args, **kwargs)

    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Guardia de Seguridad"
        verbose_name_plural = "Guardias de Seguridad"