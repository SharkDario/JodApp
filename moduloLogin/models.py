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
