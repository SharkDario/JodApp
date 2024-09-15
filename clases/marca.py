from django.db import models

class Marca(models.Model):
    _nombre = models.CharField(max_length=100, verbose_name="Nombre")

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    def __str__(self):
        return f"{self.nombre}"

    class Meta:
        app_label = 'modulo_stock'
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"