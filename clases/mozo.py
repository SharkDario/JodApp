from django.db import models
from .empleado import Empleado

class Mozo(Empleado):

    class Meta:
        app_label = 'moduloLogin'


