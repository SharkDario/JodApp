# Generated by Django 5.1 on 2024-09-13 19:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_nombre', models.CharField(max_length=100)),
                ('_descripcion', models.CharField(max_length=100)),
                ('_edad_minima', models.PositiveIntegerField(default=18)),
                ('_edad_maxima', models.PositiveIntegerField(default=40)),
            ],
            options={
                'verbose_name': 'Evento',
                'verbose_name_plural': 'Eventos',
            },
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_coordenadas', models.CharField(max_length=50, verbose_name='Coordenadas')),
                ('_descripcion', models.CharField(max_length=100, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Ubicación',
                'verbose_name_plural': 'Ubicaciones',
            },
        ),
        migrations.CreateModel(
            name='Fiesta',
            fields=[
                ('evento_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='modulo_evento.evento')),
                ('_vestimenta', models.CharField(choices=[('Formal', 'Formal'), ('Casual', 'Casual'), ('Streetwear', 'Streetwear'), ('Disfraz Tematico', 'Disfraz Temático')], max_length=20)),
                ('_categoria', models.CharField(choices=[('Tematica', 'Temática'), ('Electronica', 'Electrónica'), ('Reggaeton', 'Reggaetón'), ('Pop & Hits', 'Pop & Hits'), ('Latino', 'Latino'), ('Trap', 'Trap'), ('Fiesta Retro', 'Fiesta Retro'), ('VIP Exclusive', 'VIP Exclusive')], max_length=20)),
            ],
            options={
                'verbose_name': 'Fiesta',
                'verbose_name_plural': 'Fiestas',
            },
            bases=('modulo_evento.evento',),
        ),
        migrations.AddField(
            model_name='evento',
            name='_ubicacion',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='modulo_evento.ubicacion', verbose_name='Ubicación'),
        ),
    ]