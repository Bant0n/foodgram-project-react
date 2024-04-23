from django_restframework_base64_image_field.base64_image_field import (
    Base64ImageField,
)
from ingredients.models import IngredientsAmount
from ingredients.serializers import AmountIngredients, ReadIngredientSerializer
from rest_framework import serializers
from tags.serializers import TagSerializer
from users.serializers import UserSerializer

from .models import Recipes


class RecipesSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    author = UserSerializer()
    ingredients = ReadIngredientSerializer(
        many=True, source="recipe_ingredients"
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipes
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            'is_favorited',
            'is_in_shopping_cart',
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_in_shopping_cart(self, obj):
        return False

    def get_is_favorited(self, obj):
        return False


class RecipesCreateSerializer(serializers.ModelSerializer):
    ingredients = AmountIngredients(many=True)
    image = Base64ImageField()

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

    def to_representation(self, instance):
        serializer = RecipesSerializer(instance, context=self.context)
        return serializer.data

    def create(self, validated_data):
        ingredients_data = validated_data.pop("ingredients")
        tags_data = validated_data.pop("tags")
        recipe = Recipes.objects.create(**validated_data)
        IngredientsAmount.objects.bulk_create(
            [
                IngredientsAmount(
                    ingredient=ingredient["id"],
                    recipe=recipe,
                    amount=ingredient["amount"],
                )
                for ingredient in ingredients_data
            ]
        )
        recipe.tags.set(tags_data)
        return recipe

    def update(self, instance, validated_data):

        tags_data = validated_data.pop("tags", instance.tags)

        ingredients_data = validated_data.pop(
            "ingredients", instance.ingredients
        )

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        instance.save()

        if tags_data is not None:

            instance.tags.set(tags_data)

        if ingredients_data is not None:

            instance.ingredients.set(ingredients_data)

        return instance
