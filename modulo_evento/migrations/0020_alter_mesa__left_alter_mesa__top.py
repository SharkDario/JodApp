# Generated by Django 5.1.1 on 2024-09-26 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_evento', '0019_remove_fiesta__publicada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mesa',
            name='_left',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Posición Left'),
        ),
        migrations.AlterField(
            model_name='mesa',
            name='_top',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Posición Top'),
        ),
    ]