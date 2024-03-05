# Generated by Django 3.2 on 2024-03-05 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0002_alter_ingredients_measurement_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='measurement_unit',
            field=models.CharField(choices=[('л', 'л'), ('г', 'г'), ('кг', 'кг'), ('мл', 'мл'), ('шт', 'шт')], max_length=4, verbose_name='Единицы измерения'),
        ),
    ]