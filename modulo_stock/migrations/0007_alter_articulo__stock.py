# Generated by Django 5.1 on 2024-09-12 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modulo_stock', '0006_alter_articulo__nombre_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articulo',
            name='_stock',
            field=models.PositiveIntegerField(default=0, verbose_name='Stock'),
        ),
    ]