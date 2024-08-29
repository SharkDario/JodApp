from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from clases.persona import Persona
from clases.empleado import Empleado
from clases.contratacion import Contratacion
from clases.turno import Turno
from clases.empleado_tiene_turno import EmpleadoTieneTurno
from clases.seguridad import Seguridad
from clases.auditor import Auditor
from clases.supervisor import Supervisor
from clases.bartender import Bartender
from clases.mozo import Mozo
from clases.cajero import Cajero
from clases.administrador import Administrador

"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Persona(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20, unique=True)
    cuil = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Empleado(Persona):
    ZONA_CHOICES = [
        ('Planta baja', 'Planta baja'),
        ('Primer piso', 'Primer piso'),
    ]
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Inactivo', 'Inactivo'),
    ]
    SENIORITY_CHOICES = [
        ('Trainee', 'Trainee'),
        ('Junior', 'Junior'),
        ('Senior', 'Senior'),
    ]

    zona_asignada = models.CharField(max_length=100, choices=ZONA_CHOICES)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=ESTADO_CHOICES)
    telefono = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    seniority = models.CharField(max_length=50, choices=SENIORITY_CHOICES)
    annos_experiencia = models.PositiveIntegerField()

    def asignar_turno(self, turno):
        pass

    def calcular_estado(self):
        pass

    def calcular_sueldo(self):
        pass

class Contratacion(models.Model):
    administrador = models.ForeignKey('Administrador', on_delete=models.CASCADE, related_name='contrataciones_administradas')
    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE, related_name='contrataciones')
    fecha_contratacion = models.DateField(default=timezone.now)

    def finalizar_contrato(self):
        pass

    def renovar_contrato(self):
        pass

    def __str__(self):
        return f"{self.administrador} contrató a {self.empleado} el {self.fecha_contratacion}"

class Turno(models.Model):
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()

    def cambiar_horario(self, hora_inicio, hora_fin):
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.save()

class EmpleadoTieneTurno(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)

# Clases Especializadas
class Seguridad(Empleado):
    entrada_asignada = models.CharField(max_length=100)

class Auditor(Empleado):
    frecuencia = models.PositiveIntegerField()

class Supervisor(Empleado):
    frecuencia = models.PositiveIntegerField()

class Bartender(Empleado):
    barra_asignada = models.CharField(max_length=100)

class Mozo(Empleado):
    pass

class Cajero(Empleado):
    caja_asignada = models.CharField(max_length=100)

class Administrador(Empleado):
    cantidad_empleados_contratados = models.IntegerField(default=0)
    cantidad_fiestas_organizadas = models.IntegerField(default=0)

    def contratar_empleado(self, user, empleado_tipo, **kwargs):
        
        #Método para contratar un empleado de un tipo específico.
        #:param user: El usuario asociado al empleado
        #:param empleado_tipo: La clase del tipo de empleado a crear (subclase de Empleado)
        #:param kwargs: Argumentos adicionales para crear el empleado
        
        if not issubclass(empleado_tipo, Empleado):
            raise ValueError("Tipo de empleado no permitido")

        empleado = empleado_tipo.objects.create(user=user, **kwargs)
        self.cantidad_empleados_contratados += 1
        self.save()

        # Registrar la contratación
        Contratacion.objects.create(administrador=self, empleado=empleado)
        return empleado

    def crear_fiesta(self):
        
        #Método para registrar una fiesta organizada.
        
        self.cantidad_fiestas_organizadas += 1
        self.save()

"""