from django.db import models
from django.contrib.auth.models import User

class Persona(models.Model):
    _user = models.OneToOneField(User, on_delete=models.CASCADE)
    _dni = models.CharField(max_length=20, unique=True)
    _cuil = models.CharField(max_length=20, unique=True)
    _nombre = models.CharField(max_length=100)
    _apellido = models.CharField(max_length=100)
    _fecha_nacimiento = models.DateField()

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, value):
        self._user = value

    @property
    def dni(self):
        return self._dni

    @dni.setter
    def dni(self, value):
        self._dni = value

    @property
    def cuil(self):
        return self._cuil

    @cuil.setter
    def cuil(self, value):
        self._cuil = value

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    @property
    def apellido(self):
        return self._apellido

    @apellido.setter
    def apellido(self, value):
        self._apellido = value

    @property
    def fecha_nacimiento(self):
        return self._fecha_nacimiento

    @fecha_nacimiento.setter
    def fecha_nacimiento(self, value):
        self._fecha_nacimiento = value

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    class Meta:
        app_label = 'moduloLogin'
