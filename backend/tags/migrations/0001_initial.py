# Generated by Django 3.2 on 2024-02-29 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('color', models.CharField(blank=True, max_length=8)),
                ('slug', models.SlugField(blank=True)),
            ],
        ),
    ]