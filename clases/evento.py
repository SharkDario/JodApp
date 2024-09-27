from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models

class Evento(models.Model):
    _nombre = models.CharField(verbose_name="Nombre", max_length=100)
    _descripcion = models.CharField(verbose_name="Descripción", max_length=100)
    _edad_minima = models.PositiveIntegerField(verbose_name="Edad mínima", default=18) 
    _edad_maxima = models.PositiveIntegerField(verbose_name="Edad máxima", default=40)
    _fecha = models.DateField(verbose_name="Fecha", default=timezone.now)
    latitud = models.DecimalField(max_digits=12, decimal_places=4, default=-26.1855)
    longitud = models.DecimalField(max_digits=12, decimal_places=4, default=-58.1739)

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    @property
    def fecha(self):
        return self._fecha
    
    @fecha.setter
    def fecha(self, value):
        self._fecha = value

    @property
    def descripcion(self):
        return self._descripcion
    
    @descripcion.setter
    def descripcion(self,value):
        self._descripcion = value

    @property
    def edad_minima(self):
        return self._edad_minima
    
    @edad_minima.setter
    def edad_minima(self,value):
        self._edad_minima = value

    @property
    def edad_maxima(self):
        return self._edad_maxima
    
    @edad_maxima.setter
    def edad_maxima(self,value):
        self._edad_maxima = value

    def __str__(self):
        return f"{self.nombre} ({self.fecha})"
    
    def clean(self):
        if self._edad_minima >= self._edad_maxima:
            raise ValidationError("La edad mínima debe ser menor que la edad máxima.")

    class Meta:
        app_label = 'modulo_evento'
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
