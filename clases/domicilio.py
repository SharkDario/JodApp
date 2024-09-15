from django.db import models
from cities_light.models import City
from .persona import Persona

class Domicilio(models.Model):
    _propietario = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name="Propietario")
    _calle = models.CharField(max_length=100, verbose_name="Calle")
    _numero = models.PositiveBigIntegerField(verbose_name="Número")
    _codigo_postal = models.CharField(max_length=10, verbose_name="Código Postal")
    _ciudad = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Ciudad")
    
    @property
    def propietario(self):
        return self._propietario

    @property
    def calle(self):
        return self._calle
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def codigo_postal(self):
        return self._codigo_postal
    
    @property
    def ciudad(self):
        return self._ciudad

    @calle.setter
    def calle(self, value):
        self._calle = value

    @numero.setter
    def numero(self, value):
        self._numero = value
    
    @codigo_postal.setter
    def codigo_postal(self, value):
        self._codigo_postal = value
    
    @ciudad.setter
    def ciudad(self, value):
        self._ciudad = value

    @propietario.setter
    def propietario(self, value):
        self._propietario = value

    def __str__(self):
        return f"{self.calle} {self.numero} ({self.ciudad})"
    
    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Domicilio"
        verbose_name_plural = "Domicilios"
