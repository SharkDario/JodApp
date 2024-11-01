from django.db import models
from django.contrib.auth.models import User

class PersonaManager(models.Manager):
    def get_queryset(self):
        # Sobrescribir el queryset para que use los nombres de campo con guion bajo
        return super().get_queryset()

    def filter_by_dni(self, dni):
        # Permite filtrar por _dni utilizando el manager personalizado
        return self.get_queryset().filter(_dni=dni)

    def filter_by_cuil(self, cuil):
        # Permite filtrar por _cuil utilizando el manager personalizado
        return self.get_queryset().filter(_cuil=cuil)
    
    def filter_by_user(self, user):
        # Permite filtrar por _user utilizando el manager personalizado
        return self.get_queryset().filter(_user=user)

class Persona(models.Model):
    #PBKDF2 (Password-Based Key Derivation Function 2) con un SHA256 hash
    _user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    _dni = models.CharField(max_length=20, unique=True, verbose_name="DNI")
    _cuil = models.CharField(max_length=20, unique=True, verbose_name="CUIL")
    _nombre = models.CharField(max_length=100, verbose_name="Nombre")
    _apellido = models.CharField(max_length=100, verbose_name="Apellido")
    _fecha_nacimiento = models.DateField(verbose_name="Fecha de nacimiento")

    objects = PersonaManager()  # Usar el manager personalizado

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
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
