# Generated by Django 5.1 on 2024-09-12 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moduloLogin', '0010_domicilio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domicilio',
            name='_pais',
        ),
    ]
