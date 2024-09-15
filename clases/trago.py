from django.db import models
from .articulo import Articulo

class Trago(Articulo):
    _tipo = models.CharField(verbose_name="Tipo", max_length=50, choices=[('Cóctel', 'Cóctel'), ('Shot', 'Shot'), ('Licuado', 'Licuado')])

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, value):
        self._tipo = value

    # Método para actualizar el volumen del trago basado en los ingredientes
    def actualizar_volumen(self):
        total_volumen = sum(fabricacion.cantidad_producto for fabricacion in self.fabricacion_set.all())
        self._volumen = total_volumen
        self.save()

    def actualizar_stock(self):
        # Calcula el stock disponible en función de los ingredientes (fabricación)
        total_stock = None

        # Recorre todas las fabricaciones asociadas al trago
        for fabricacion in self.fabricacion_set.all():
            # Stock del producto utilizado en la fabricación
            stock_producto = fabricacion._producto._stock
            volumen_producto = fabricacion._producto._volumen
            stock_producto = stock_producto * volumen_producto
            cantidad_usada_por_trago = fabricacion._cantidad_producto

            # Calcula cuántas unidades del trago se pueden hacer con el stock del producto
            stock_posible_con_producto = stock_producto // cantidad_usada_por_trago

            # Si total_stock es None (primera iteración), inicialízalo, sino calcula el mínimo
            if total_stock is None:
                total_stock = stock_posible_con_producto
            else:
                total_stock = min(total_stock, stock_posible_con_producto)

        # Si no hay fabricación, no hay stock
        if total_stock is None:
            total_stock = 0

        self._stock = total_stock
        self.save()

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

    class Meta:
        app_label = 'modulo_stock'
        verbose_name = "Trago"
        verbose_name_plural = "Tragos"
