# Generated by Django 5.1.1 on 2024-09-19 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moduloLogin', '0014_alter_empleado__annos_experiencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='_annos_experiencia',
            field=models.PositiveIntegerField(verbose_name='Años de experiencia'),
        ),
    ]