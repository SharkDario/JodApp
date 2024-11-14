from django.db import models



class MejoresClientes(models.Model):
    """
    Modelo que se conecta a la vista view_mejores_clientes existente
    """
    id = models.IntegerField(primary_key=True, verbose_name="DNI")
    _nombre = models.CharField(db_column='_nombre', max_length=255, verbose_name="Nombre")
    _apellido = models.CharField(db_column='_apellido', max_length=255, verbose_name="Apellido")
    numero_compras = models.IntegerField(verbose_name="Número de compras")
    monto_total_gastado = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Total Gastado")
    _fecha_emision = models.DateTimeField(db_column='_fecha_emision', verbose_name="Fecha de Emisión")

    class Meta:
        managed = False
        db_table = 'view_mejores_clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Mejores Clientes'
        # Definimos la clave primaria compuesta
        unique_together = ('id', '_fecha_emision')

class ProductosMasVendidos(models.Model):
    """
    Modelo que se conecta a la vista view_productos_mas_vendidos existente
    """
    id = models.IntegerField(primary_key=True, verbose_name="ID")
    producto = models.CharField(max_length=255, verbose_name="Producto")
    cantidad_total_vendida = models.IntegerField(verbose_name="Cantidad Total Vendida")
    monto_total_ventas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Total de la Venta")
    _fecha_emision = models.DateTimeField(db_column='_fecha_emision', verbose_name="Fecha de Emisión")

    class Meta:
        managed = False
        db_table = 'view_productos_mas_vendidos'
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos Más Vendidos'

class EntradasFiesta(models.Model):
    """
    Modelo que se conecta a la vista view_entradas_fiesta existente
    """
    evento_id = models.IntegerField(primary_key=True, verbose_name="ID")
    nombre_evento = models.CharField(max_length=255, verbose_name="Nombre de Fiesta")
    fecha = models.DateField(verbose_name="Fecha")
    total_entradas_vendidas = models.IntegerField(verbose_name="Total de Entradas Vendidas")
    categoria = models.CharField(max_length=255, verbose_name="Categoría")
    monto_total_ventas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Total de Ventas")

    class Meta:
        managed = False  # Django no administra esta tabla
        db_table = 'view_entradas_fiesta'
        verbose_name = 'Fiesta'
        verbose_name_plural = 'Total de Entradas por Fiesta'

class ReservacionesFiesta(models.Model):
    """
    Modelo que se conecta a la vista view_reservaciones_fiesta existente
    """
    id = models.IntegerField(primary_key=True, verbose_name="ID")
    nombre_evento = models.CharField(max_length=255, verbose_name="Nombre de Fiesta")
    fecha = models.DateField(verbose_name="Fecha")
    total_reservaciones = models.IntegerField(verbose_name="Total de Reservaciones")
    categoria = models.CharField(max_length=255, verbose_name="Categoría")
    monto_total_ventas = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto Total de Ventas")

    class Meta:
        managed = False
        db_table = 'view_reservaciones_fiesta'
        verbose_name = 'Fiesta'
        verbose_name_plural = 'Total de Reservaciones por Fiesta'