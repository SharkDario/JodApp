from django.db import models

class TipoFacturaManager(models.Manager):
    def get_queryset(self):
        # Sobrescribir el queryset para que use los nombres de campo con guion bajo
        return super().get_queryset()
    
    def filter_by_descripcion(self, descripcion):
        # Permite filtrar por _dni utilizando el manager personalizado
        return self.get_queryset().filter(_descripcion=descripcion)

class TipoFactura(models.Model):
    _descripcion = models.CharField(verbose_name="Descripción", max_length=100)

    objects = TipoFacturaManager()  # Usar el manager personalizado

    @property
    def descripcion(self):
        return self._descripcion

    @descripcion.setter
    def descripcion(self, value):
        self._descripcion = value

    def __str__(self):
        return f"{self.descripcion}"

    class Meta:
        app_label = 'modulo_ventas'
        verbose_name = "Tipo Factura"
        verbose_name_plural = "Tipos Factura"
