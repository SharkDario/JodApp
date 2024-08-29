from django.db import models
from .empleado import Empleado

class Administrador(Empleado):
    #cantidad_empleados_contratados = models.IntegerField(default=0)
    #cantidad_fiestas_organizadas = models.IntegerField(default=0)

    class Meta:
        app_label = 'moduloLogin'

    @property
    def cantidad_empleados_contratados(self):
        from .contratacion import Contratacion
        # Asumimos que tienes un modelo Contratacion con un campo administrador
        return Contratacion.objects.filter(administrador=self).count()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

   # @property
    #def cantidad_fiestas_organizadas(self):
        #from .fiesta import Fiesta
        # Asumimos que tienes un modelo Fiesta con un campo organizador
        #return Fiesta.objects.filter(organizador=self).count()