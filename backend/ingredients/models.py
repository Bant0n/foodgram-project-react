from django.db import models
from recipes.models import Recipes


class Ingredients(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название")
    measurement_unit = models.CharField(
        max_length=32,
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


class IngredientsAmount(models.Model):
    ingredient = models.ForeignKey(
        Ingredients, on_delete=models.CASCADE, verbose_name="Ингредиетн",
        related_name='ingredients_amount'
    )
    amount = models.PositiveIntegerField(
        blank=False, verbose_name="Количество"
    )
    recipe = models.ForeignKey(
        Recipes, on_delete=models.CASCADE, verbose_name="Рецепт",
        related_name='recipe_ingredients'
    )

    def __str__(self):
        return (f'В рецепте "{self.recipe}" '
                f'кол-во "{self.ingredient}" ровна "{self.amount}"')
