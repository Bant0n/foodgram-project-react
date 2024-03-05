from django.db import models


class Ingredients(models.Model):
    MEASUREMENT_UNIT = {
        ("г", "г"),
        ("кг", "кг"),
        ("л", "л"),
        ("мл", "мл"),
        ("шт", "шт"),
    }
    name = models.CharField(max_length=64, verbose_name="Название")
    amount = models.PositiveIntegerField(
        blank=False, verbose_name="Количество"
    )
    measurement_unit = models.CharField(
        choices=MEASUREMENT_UNIT,
        max_length=4,
        verbose_name="Единицы измерения",
    )

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"
        ordering = ["name"]
        constraints = (
            models.UniqueConstraint(
                fields=("name", "measurement_unit"), name="unique_ingredient"
            ),
        )

    def __str__(self):
        return self.name
