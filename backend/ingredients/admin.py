from django.contrib import admin

from .models import Ingredients, IngredientsAmount


admin.site.register(Ingredients)
admin.site.register(IngredientsAmount)
