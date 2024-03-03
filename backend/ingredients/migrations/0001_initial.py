# Generated by Django 3.2 on 2024-02-29 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('amount', models.PositiveIntegerField()),
                ('measurement_unit', models.CharField(choices=[('шт', 'шт'), ('мл', 'мл'), ('г', 'г'), ('кг', 'кг'), ('л', 'л')], max_length=4)),
            ],
        ),
    ]
