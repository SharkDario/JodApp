from django.db import models
from .persona import Persona

class Cliente(Persona):
    _embedding = models.JSONField(blank=True, null=True)
    _foto = models.ImageField(upload_to='fotos_clientes/', blank=True, null=True)

    @property
    def embedding(self):
        return self._embedding

    @embedding.setter
    def embedding(self, value):
        if isinstance(value, list) and all(isinstance(v, (float, int)) for v in value):
            self._embedding = value
        else:
            raise ValueError("El embedding debe ser una lista de números.")
        
    @property
    def foto(self):
        return self._foto

    @foto.setter
    def foto(self, value):
        self._foto = value
        
    def __str__(self):
        return f"{self.nombre} {self.apellido} (Cliente)"
    
    class Meta:
        app_label = 'modulo_clientes'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"