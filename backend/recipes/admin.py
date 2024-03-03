from django.contrib import admin

from .models import Recipes, FavoriteRecipe, ShoppingCart


admin.site.register(Recipes)
admin.site.register(FavoriteRecipe)
admin.site.register(ShoppingCart)
