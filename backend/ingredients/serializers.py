from rest_framework import serializers

from .models import Ingredients


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ("id", "name", "amount", "measurement_unit")


class CreateIngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ("id", "amount",)
