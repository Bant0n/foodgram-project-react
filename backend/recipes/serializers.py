from drf_extra_fields.fields import Base64ImageField
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
            "is_favorited",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return user.shoppingcart_set.filter(recipes=obj).exists()

    def get_is_favorited(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return user.favoriterecipe_set.filter(recipes=obj).exists()


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

    def validate_image(self, value):
        if not value:
            raise serializers.ValidationError(
                "Необходимо добавить изображение"
            )

        return value

    def validate_cooking_time(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Время приготовления должно быть больше нуля"
            )
        return value

    def validate_ingredients(self, value):

        if not value:
            raise serializers.ValidationError(
                "Необходимо добавить ингредиенты"
            )
        return value

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
        ingredients_data = validated_data.pop("ingredients")
        tags_data = validated_data.pop("tags")
        for tags in tags_data:
            instance.tags.clear()
            instance.tags.add(tags)

        instance.ingredients.clear()
        IngredientsAmount.objects.bulk_create(
            [
                IngredientsAmount(
                    ingredient=ingredient["id"],
                    recipe=instance,
                    amount=ingredient["amount"],
                )
                for ingredient in ingredients_data
            ]
        )
        return instance


class ShortRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )
