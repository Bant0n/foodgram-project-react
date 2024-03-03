from ingredients.models import Ingredients
from ingredients.serializers import (
    IngredientsSerializer,
    CreateIngredientsSerializer,
)
from rest_framework import serializers
from tags.models import Tag
from tags.serializers import TagSerializer, CreateTagSerializer
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

    # def create(self, validated_data):
    #     print(validated_data)
    #     tags_data = validated_data.pop("tags")
    #     ingredients_data = validated_data.pop("ingredients")
    #     recipe = Recipes.objects.create(**validated_data)

    #     for tag_data in tags_data:
    #         tag, created = Tag.objects.get_or_create(**tag_data)
    #         recipe.tags.add(tag)

    #     for ingredient_data in ingredients_data:
    #         ingredient, created = Ingredients.objects.get_or_create(
    #             **ingredient_data
    #         )
    #         recipe.ingredients.add(ingredient)
    #         print(ingredient)

    #     return recipe

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.image = validated_data.get("image", instance.image)
    #     instance.text = validated_data.get("text", instance.text)
    #     instance.cooking_time = validated_data.get(
    #         "cooking_time", instance.cooking_time
    #     )

    #     tags_data = validated_data.get("tags")
    #     if tags_data:
    #         instance.tags.clear()
    #         for tag_data in tags_data:
    #             tag, created = Tag.objects.get_or_create(**tag_data)
    #             instance.tags.add(tag)

    #     ingredients_data = validated_data.get("ingredients")
    #     if ingredients_data:
    #         instance.ingredients.clear()
    #         for ingredient_data in ingredients_data:
    #             ingredient, created = Ingredients.objects.get_or_create(
    #                 **ingredient_data
    #             )
    #             instance.ingredients.add(ingredient)

    #     instance.save()
    #     return instance


class RecipesCreateSerializer(serializers.ModelSerializer):
    tags = CreateTagSerializer(many=True)
    ingredients = CreateIngredientsSerializer(many=True)

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
        print(validated_data)
        tags_data = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients")
        recipe = Recipes.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(**tag_data)
            recipe.tags.add(tag)

        for ingredient_data in ingredients_data:
            ingredient, created = Ingredients.objects.get_or_create(
                **ingredient_data
            )
            recipe.ingredients.add(ingredient)
            print(ingredient)

        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )

        tags_data = validated_data.get("tags")
        if tags_data:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(**tag_data)
                instance.tags.add(tag)

        ingredients_data = validated_data.get("ingredients")
        if ingredients_data:
            instance.ingredients.clear()
            for ingredient_data in ingredients_data:
                ingredient, created = Ingredients.objects.get_or_create(
                    **ingredient_data
                )
                instance.ingredients.add(ingredient)

        instance.save()
        return instance
