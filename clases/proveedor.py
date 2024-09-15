from django.db import models
from .persona import Persona

class Proveedor(Persona):
    _condicion_iva = models.CharField(verbose_name="Condición IVA", max_length=50, choices=[('Responsable Inscripto', 'Responsable Inscripto'), ('Monotributista', 'Monotributista'), ('Exento', 'Exento')], default='Responsable Inscripto')

    @property
    def condicion_iva(self):
        return self._condicion_iva

    @condicion_iva.setter
    def condicion_iva(self, value):
        self._condicion_iva = value

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Proveedor)"

    class Meta:
        app_label = 'modulo_stock'
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"