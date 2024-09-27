# Generated by Django 5.1.1 on 2024-09-26 21:01

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moduloLogin', '0015_alter_empleado__annos_experiencia'),
        ('modulo_evento', '0023_alter_mesa_options_alter_mesatienearticulo_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientoFiesta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_fecha', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha')),
                ('_descripcion', models.CharField(choices=[('registró', 'registró'), ('modificó', 'modificó')], max_length=20, verbose_name='Descripción')),
                ('_administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moduloLogin.administrador', verbose_name='Administrador')),
                ('_fiesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='modulo_evento.fiesta', verbose_name='Fiesta')),
            ],
            options={
                'verbose_name': 'Movimientos de Fiestas',
                'verbose_name_plural': 'Movimientos de Fiestas',
                'ordering': ['_fecha', '_fiesta___fecha', '_fiesta___nombre', '_administrador___nombre', '_administrador___apellido'],
            },
        ),
    ]
