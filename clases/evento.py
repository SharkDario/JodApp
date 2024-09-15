from django.core.exceptions import ValidationError
from django.db import models
#from mapbox_location_field.models import LocationField  # Asegúrate de tener la dependencia

class Evento(models.Model):
    _nombre = models.CharField(max_length=100)
    _descripcion = models.CharField(max_length=100)
    _edad_minima = models.PositiveIntegerField(default=18) 
    _edad_maxima = models.PositiveIntegerField(default=40)
    _latitud = models.DecimalField(max_digits=9, decimal_places=6, default=-26.1849)
    _longitud = models.DecimalField(max_digits=9, decimal_places=6, default=-58.1731)

    @property
    def latitud(self):
        return self._latitud
    
    @latitud.setter
    def latitud(self, value):
        self._latitud = value

    @property
    def longitud(self):
        return self._longitud
    
    @longitud.setter
    def longitud(self, value):
        self._longitud = value

    @property
    def nombre(self):
        return self._nombre
    
    @nombre.setter
    def nombre(self, value):
        self._nombre = value

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
        return f"{self.nombre} ({self.descripcion})"
    
    def clean(self):
        if self._edad_minima >= self._edad_maxima:
            raise ValidationError("La edad mínima debe ser menor que la edad máxima.")

    class Meta:
        app_label = 'modulo_evento'
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
