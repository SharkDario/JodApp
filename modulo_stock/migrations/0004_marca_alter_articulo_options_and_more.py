# Generated by Django 5.1 on 2024-09-11 18:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_stock', '0003_detalleremitoproveedor__estado_producto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_nombre', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Marca',
                'verbose_name_plural': 'Marcas',
            },
        ),
        migrations.AlterModelOptions(
            name='articulo',
            options={'verbose_name': 'Artículo', 'verbose_name_plural': 'Artículos'},
        ),
        migrations.AlterModelOptions(
            name='detalleremitoproveedor',
            options={'verbose_name': 'Detalle Remito (Proveedor)', 'verbose_name_plural': 'Detalles Remito (Proveedor)'},
        ),
        migrations.AlterModelOptions(
            name='estadoproducto',
            options={'verbose_name': 'Estado de Producto', 'verbose_name_plural': 'Estados de Producto'},
        ),
        migrations.AlterModelOptions(
            name='fabricacion',
            options={'verbose_name': 'Coctelería', 'verbose_name_plural': 'Coctelerías'},
        ),
        migrations.AlterModelOptions(
            name='movimientostock',
            options={'verbose_name': 'Movimiento de stock', 'verbose_name_plural': 'Movimientos de stock'},
        ),
        migrations.AlterModelOptions(
            name='producto',
            options={'verbose_name': 'Producto', 'verbose_name_plural': 'Productos'},
        ),
        migrations.AlterModelOptions(
            name='proveedor',
            options={'verbose_name': 'Proveedor', 'verbose_name_plural': 'Proveedores'},
        ),
        migrations.AlterModelOptions(
            name='remitoproveedor',
            options={'verbose_name': 'Remito (Proveedor)', 'verbose_name_plural': 'Remitos (Proveedor)'},
        ),
        migrations.AlterModelOptions(
            name='trago',
            options={'verbose_name': 'Trago', 'verbose_name_plural': 'Tragos'},
        ),
        migrations.AlterField(
            model_name='producto',
            name='_marca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_stock.marca'),
        ),
    ]