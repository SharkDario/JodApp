from django.db import models
from django.core.validators import MinValueValidator
from .fiesta import Fiesta

class MesaManager(models.Manager):
    def get_queryset(self):
        # Sobrescribir el queryset para que use los nombres de campo con guion bajo
        return super().get_queryset()

    def filter_by_fiesta(self, fiesta):
        # Permite filtrar por _dni utilizando el manager personalizado
        return self.get_queryset().filter(_fiesta=fiesta)

class Mesa(models.Model):
    CATEGORIA_CHOICES = [
        ('Popular', 'Popular'),
        ('VIP', 'VIP'),
    ]
    _fiesta = models.ForeignKey(Fiesta, on_delete=models.CASCADE, verbose_name="Fiesta")
    _categoria = models.CharField(verbose_name="Categoría", max_length=20, choices=CATEGORIA_CHOICES)
    _capacidad = models.PositiveIntegerField(verbose_name="Capacidad", default=8)
    _precio = models.DecimalField(verbose_name="Precio", max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    _disponibilidad = models.BooleanField(verbose_name="Disponibilidad", default=True)
    _top = models.PositiveIntegerField(verbose_name="Posición Top", default=0, editable=False)  # Coordenada top
    _left = models.PositiveIntegerField(verbose_name="Posición Left", default=0, editable=False)  # Coordenada left
    
    objects = MesaManager()  # Usar el manager personalizado

    @property
    def precio(self):
        return self._precio
    
    @precio.setter
    def precio(self, value):
        self._precio = value

    @property
    def top(self):
        return self._top

    @top.setter
    def top(self, value):
        self._top = value

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value

    @property
    def capacidad(self):
        return self._capacidad
    
    @capacidad.setter
    def capacidad(self,value):
        self._capacidad = value

    @property
    def fiesta(self):
        return self._fiesta
    
    @fiesta.setter
    def fiesta(self,value):
        self._fiesta = value

    @property
    def categoria(self):
        return self._categoria
    
    @categoria.setter
    def categoria(self,value):
        self._categoria = value

    @property
    def disponibilidad(self):
        return "Disponible" if self._disponibilidad else "Reservada"

    @disponibilidad.setter
    def disponibilidad(self, value):
        if isinstance(value, bool):
            self._disponibilidad = value
        else:
            raise ValueError("El valor de disponibilidad debe ser un booleano.")
        
    @property
    def color(self):
        return "green" if self._disponibilidad else "red"
    
    @property
    def numero(self):
        try:
            # Obtener todas las mesas relacionadas con la misma fiesta
            mesas = list(self._fiesta.mesa_set.order_by('id'))
            # Retornar el índice de la mesa actual +1 para que empiece en 1
            return mesas.index(self) + 1
        except ValueError:
            return "(actualizar)"
    
    def __str__(self):
        return f"Mesa [{self.numero}] [{self.fiesta}]"

    class Meta:
        app_label = 'modulo_evento'
        verbose_name = "Gestión de Mesas"
        verbose_name_plural = "Gestión de Mesas"
        ordering = ['_fiesta___fecha', '_fiesta___nombre']