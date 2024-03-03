from django.contrib.auth import get_user_model
from django.db import models
from ingredients.models import Ingredients
from tags.models import Tag

User = get_user_model()


class Recipes(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to='recipes/', null=True, blank=True)
    text = models.TextField()
    ingredients = models.ManyToManyField(Ingredients)
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.recipes.name


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE)

    def __str__(self):
        return self.recipes.name
