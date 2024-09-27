from django.utils import timezone
from django.db import models
from .fiesta import Fiesta
from .administrador import Administrador

class MovimientoFiesta(models.Model):
    _fiesta = models.ForeignKey(Fiesta, on_delete=models.CASCADE, verbose_name="Fiesta")
    _administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE, verbose_name="Administrador")
    _fecha = models.DateField(verbose_name="Fecha", default=timezone.now)
    _descripcion = models.CharField(verbose_name="Descripción", max_length=300)
    
    @property
    def fiesta(self):
        return self._fiesta
    
    @fiesta.setter
    def fiesta(self,value):
        self._fiesta = value

    @property
    def administrador(self):
        return self._administrador
    
    @administrador.setter
    def administrador(self,value):
        self._administrador = value

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
    
    def __str__(self):
        return f"{self.administrador} {self.descripcion} la {self.fiesta} ({self.fecha})"

    class Meta:
        app_label = 'modulo_evento'
        verbose_name = "Movimientos de Fiestas"
        verbose_name_plural = "Movimientos de Fiestas"
        ordering = ['-_fecha', '-_fiesta___fecha', '_fiesta___nombre', '_administrador___nombre', '_administrador___apellido']