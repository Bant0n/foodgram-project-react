from ingredients.models import Ingredients
from ingredients.serializers import (
    IngredientsSerializer,
)
from rest_framework import serializers
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import UserSerializer

from .models import Recipes


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientsSerializer(many=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipes
        fields = (
            "id",
            "author",
            "name",
            "image",
            "text",
            "cooking_time",
            "tags",
            "ingredients",
        )
        read_only_fields = ("id", "author")


class RecipesCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(), many=True
    )

    class Meta:
        model = Recipes
        fields = (
            "ingredients",
            "tags",
            "image",
            "name",
            "text",
            "cooking_time",
        )

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        ingredients_data = validated_data.pop("ingredients", [])

        recipe = Recipes.objects.create(**validated_data)

        recipe.tags.set(tags_data)
        recipe.ingredients.set(ingredients_data)

        return recipe

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        ingredients_data = validated_data.pop('ingredients', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags_data is not None:
            instance.tags.set(tags_data)
        if ingredients_data is not None:
            instance.ingredients.set(ingredients_data)

        return instance
