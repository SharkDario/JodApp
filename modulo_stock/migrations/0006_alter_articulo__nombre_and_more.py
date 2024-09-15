# Generated by Django 5.1 on 2024-09-12 15:35

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moduloLogin', '0009_alter_auditor__frecuencia_and_more'),
        ('modulo_stock', '0005_alter_fabricacion_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='_nombre',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='_precio_unitario',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Precio Unitario'),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='_stock',
            field=models.PositiveIntegerField(verbose_name='Stock'),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='_stock_minimo',
            field=models.PositiveIntegerField(verbose_name='Stock Mínimo'),
        ),
        migrations.AlterField(
            model_name='articulo',
            name='_volumen',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Volumen en mililitros', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Volumen'),
        ),
        migrations.AlterField(
            model_name='detalleremitoproveedor',
            name='_cantidad',
            field=models.PositiveIntegerField(verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='detalleremitoproveedor',
            name='_estado_producto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='modulo_stock.estadoproducto', verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='detalleremitoproveedor',
            name='_fecha_entrega_producto',
            field=models.DateField(verbose_name='Fecha Entrega Producto'),
        ),
        migrations.AlterField(
            model_name='detalleremitoproveedor',
            name='_producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_stock.producto', verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='detalleremitoproveedor',
            name='_remito',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_stock.remitoproveedor', verbose_name='Remito'),
        ),
        migrations.AlterField(
            model_name='estadoproducto',
            name='_descripcion',
            field=models.CharField(max_length=100, verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='fabricacion',
            name='_cantidad_producto',
            field=models.DecimalField(decimal_places=2, max_digits=5, validators=[django.core.validators.MinValueValidator(0)], verbose_name='cantidad  (mililitros)'),
        ),
        migrations.AlterField(
            model_name='fabricacion',
            name='_producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_stock.producto', verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='fabricacion',
            name='_trago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_stock.trago', verbose_name='Trago'),
        ),
        migrations.AlterField(
            model_name='marca',
            name='_nombre',
            field=models.CharField(max_length=100, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='movimientostock',
            name='_cantidad',
            field=models.PositiveIntegerField(verbose_name='Cantidad'),
        ),
        migrations.AlterField(
            model_name='movimientostock',
            name='_empleado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moduloLogin.empleado', verbose_name='Empleado'),
        ),
        migrations.AlterField(
            model_name='movimientostock',
            name='_fecha_movimiento',
            field=models.DateField(verbose_name='Fecha de movimiento'),
        ),
        migrations.AlterField(
            model_name='movimientostock',
            name='_producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_stock.producto', verbose_name='Producto'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='_marca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_stock.marca', verbose_name='Marca'),
        ),
        migrations.AlterField(
            model_name='proveedor',
            name='_condicion_iva',
            field=models.CharField(choices=[('Responsable Inscripto', 'Responsable Inscripto'), ('Monotributista', 'Monotributista'), ('Exento', 'Exento')], default='Responsable Inscripto', max_length=50, verbose_name='Condición IVA'),
        ),
        migrations.AlterField(
            model_name='remitoproveedor',
            name='_fecha_emision_remito',
            field=models.DateField(verbose_name='Fecha de emisión'),
        ),
        migrations.AlterField(
            model_name='remitoproveedor',
            name='_numero_remito',
            field=models.CharField(max_length=100, verbose_name='Número'),
        ),
        migrations.AlterField(
            model_name='remitoproveedor',
            name='_proveedor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_stock.proveedor', verbose_name='Proveedor'),
        ),
        migrations.AlterField(
            model_name='trago',
            name='_tipo',
            field=models.CharField(choices=[('Cóctel', 'Cóctel'), ('Shot', 'Shot'), ('Licuado', 'Licuado')], max_length=50, verbose_name='Tipo'),
        ),
    ]