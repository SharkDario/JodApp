from .empleado import Empleado

class Administrador(Empleado):
    @property
    def cantidad_empleados_contratados(self):
        from .contratacion import Contratacion
        return Contratacion.objects.filter(_administrador=self, _tipo='Contratacion').count()

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.cantidad_empleados_contratados})"
    
    def save(self, *args, **kwargs):
        if self._user:
            self._user.is_superuser = True
            self._user.save()
        # Llamamos al método save original para guardar el objeto
        super().save(*args, **kwargs)
    
    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

"""
# Si es una actualización, comprobamos el estado anterior
        if self.pk:  # Si ya tiene un ID (es decir, existe en la base de datos)
            estado_anterior = Administrador.objects.get(pk=self.pk)._estado
            # Si el estado cambia de 'Inactivo' a 'Activo', marcamos el usuario como staff
            if estado_anterior == 'Inactivo' and self._estado == 'Activo':
                self._user.is_staff = True
                self._user.is_superuser = True
                self._user.save()
            # Si cambia de 'Activo' a 'Inactivo', removemos el estado de staff
            elif estado_anterior == 'Activo' and self._estado == 'Inactivo':
                self._user.is_staff = False
                self._user.is_superuser = False
                self._user.save()

"""