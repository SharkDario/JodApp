from django.db import models
from .persona import Persona

class Empleado(Persona):
    _zona_asignada = models.CharField(max_length=100, choices=[('Planta baja', 'Planta baja'), ('Primer piso', 'Primer piso')], verbose_name="Zona Asignada")
    _sueldo = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sueldo")
    _estado = models.CharField(max_length=50, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Inactivo', verbose_name="Estado")
    _fecha_inicio = models.DateField(verbose_name="Fecha Inicio")
    _seniority = models.CharField(max_length=50, choices=[('Trainee', 'Trainee'), ('Junior', 'Junior'), ('Senior', 'Senior')], verbose_name="Seniority")
    _annos_experiencia = models.PositiveIntegerField(verbose_name="Años de experiencia")

    @property
    def zona_asignada(self):
        return self._zona_asignada

    @zona_asignada.setter
    def zona_asignada(self, value):
        self._zona_asignada = value

    @property
    def sueldo(self):
        return self._sueldo

    @sueldo.setter
    def sueldo(self, value):
        self._sueldo = value

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, value):
        self._estado = value
    
    @property
    def fecha_inicio(self):
        return self._fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, value):
        self._fecha_inicio = value

    @property
    def seniority(self):
        return self._seniority

    @seniority.setter
    def seniority(self, value):
        self._seniority = value

    @property
    def annos_experiencia(self):
        return self._annos_experiencia

    @annos_experiencia.setter
    def annos_experiencia(self, value):
        self._annos_experiencia = value

    def save(self, *args, **kwargs):
        # Si es una actualización, comprobamos el estado anterior
        if self.pk:  # Si ya tiene un ID (es decir, existe en la base de datos)
            estado_anterior = Empleado.objects.get(pk=self.pk)._estado
            # Si el estado cambia de 'Inactivo' a 'Activo', marcamos el usuario como staff
            if estado_anterior == 'Inactivo' and self._estado == 'Activo':
                self._user.is_staff = True
                self._user.save()
            # Si cambia de 'Activo' a 'Inactivo', removemos el estado de staff
            elif estado_anterior == 'Activo' and self._estado == 'Inactivo':
                self._user.is_staff = False
                self._user.save()

        # Llamamos al método save original para guardar el objeto
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido} (Empleado)"

    class Meta:
        app_label = 'moduloLogin'
        verbose_name = "Empleado"
