# Generated by Django 5.1.1 on 2024-10-13 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_ventas', '0004_transaccionpago'),
    ]

    operations = [
        migrations.AddField(
            model_name='facturacliente',
            name='_pagado',
            field=models.BooleanField(default=False, verbose_name='Estado del pago'),
        ),
    ]
