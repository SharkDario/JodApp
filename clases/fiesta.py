from django.db import models
from .evento import Evento

class Fiesta(Evento):
    CATEGORIA_CHOICES = [
        ('Tematica', 'Temática'),
        ('Electronica', 'Electrónica'),
        ('Reggaeton', 'Reggaetón'),
        ('Pop & Hits', 'Pop & Hits'),
        ('Latino', 'Latino'),
        ('Trap', 'Trap'),
        ('Fiesta Retro', 'Fiesta Retro'),
        ('VIP Exclusive', 'VIP Exclusive'),
    ]

    VESTIMENTA_CHOICES = [
        ('Formal', 'Formal'),
        ('Casual', 'Casual'),
        ('Streetwear', 'Streetwear'),
        ('Disfraz Tematico', 'Disfraz Temático'),
    ]

    _vestimenta = models.CharField(max_length=20, choices=VESTIMENTA_CHOICES)
    _categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)

    @property
    def vestimenta(self):
        return self._vestimenta
    
    @vestimenta.setter
    def vestimenta(self,value):
        self._vestimenta = value

    @property
    def categoria(self):
        return self._categoria
    
    @categoria.setter
    def categoria(self,value):
        self._categoria = value

    class Meta:
        app_label = 'modulo_evento'
        verbose_name = "Fiesta"
        verbose_name_plural = "Fiestas"
    