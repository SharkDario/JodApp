from django.db import models

# Create your models here.
from django.utils import timezone

from clases.evento import Evento
from clases.fiesta import Fiesta
from clases.entrada import Entrada
from clases.mesa import Mesa
from clases.mesa_tiene_articulo import MesaTieneArticulo
from clases.movimiento_fiesta import MovimientoFiesta
from clases.administrador import Administrador