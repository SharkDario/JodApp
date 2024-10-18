# Generated by Django 5.1.1 on 2024-10-09 01:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moduloLogin', '0015_alter_empleado__annos_experiencia'),
        ('modulo_evento', '0026_remove_entrada__cliente_delete_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('persona_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='moduloLogin.persona')),
                ('_embedding', models.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
            bases=('moduloLogin.persona',),
        ),
    ]