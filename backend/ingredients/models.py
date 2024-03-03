from django.db import models


class Ingredients(models.Model):
    MEASUREMENT_UNIT = {
        ('г', 'г'),
        ('кг', 'кг'),
        ('л', 'л'),
        ('мл', 'мл'),
        ('шт', 'шт'),
    }
    name = models.CharField(max_length=64)
    amount = models.PositiveIntegerField(blank=False)
    measurement_unit = models.CharField(choices=MEASUREMENT_UNIT, max_length=4)

    def __str__(self):
        return self.name
