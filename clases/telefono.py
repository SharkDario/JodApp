from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .persona import Persona

class Telefono(models.Model):
    _propietario = models.ForeignKey(Persona, on_delete=models.CASCADE, verbose_name="Propietario")
    _numero_telefono = PhoneNumberField(verbose_name="Número de Teléfono") # "AR" para Argentina

    @property
    def numero_telefono(self):
        return self._numero_telefono
    
    @property
    def propietario(self):
        return self._propietario

    @numero_telefono.setter
    def numero_telefono(self, value):
        self._numero_telefono = value

    @propietario.setter
    def propietario(self, value):
        self._propietario = value

    def __str__(self):
        return str(self.numero_telefono)

    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Teléfono"
        verbose_name_plural = "Teléfonos"
