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

    _vestimenta = models.CharField(verbose_name="Vestimenta", max_length=20, choices=VESTIMENTA_CHOICES)
    _categoria = models.CharField(verbose_name="Categoría", max_length=20, choices=CATEGORIA_CHOICES)
    _cantidad_entrada_popular = models.PositiveIntegerField(verbose_name="Cantidad Entradas Populares", default=1)
    _cantidad_entrada_vip = models.PositiveIntegerField(verbose_name="Cantidad Entradas VIP", default=1)

    @property
    def cantidad_entrada_popular(self):
        return self._cantidad_entrada_popular
    
    @cantidad_entrada_popular.setter
    def cantidad_entrada_popular(self, value):
        self._cantidad_entrada_popular = value

    @property
    def cantidad_entrada_vip(self):
        return self._cantidad_entrada_vip
    
    @cantidad_entrada_vip.setter
    def cantidad_entrada_vip(self, value):
        self._cantidad_entrada_vip = value

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
    