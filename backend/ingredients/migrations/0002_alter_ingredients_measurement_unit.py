# Generated by Django 3.2 on 2024-02-29 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredients',
            name='measurement_unit',
            field=models.CharField(choices=[('л', 'л'), ('шт', 'шт'), ('г', 'г'), ('кг', 'кг'), ('мл', 'мл')], max_length=4),
        ),
    ]
