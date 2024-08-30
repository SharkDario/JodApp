from .empleado import Empleado

class Administrador(Empleado):
    @property
    def cantidad_empleados_contratados(self):
        from .contratacion import Contratacion
        return Contratacion.objects.filter(_administrador=self).count()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        app_label = 'moduloLogin'

   # @property
    #def cantidad_fiestas_organizadas(self):
        #from .fiesta import Fiesta
        # Asumimos que tienes un modelo Fiesta con un campo organizador
        #return Fiesta.objects.filter(organizador=self).count()