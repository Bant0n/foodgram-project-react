from rest_framework import serializers
from .models import CustomUser, Followers
from djoser.serializers import UserSerializer, UserCreateSerializer

from recipes.models import Recipes


class ShortRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipes
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class UserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return user.followers.filter(author=obj).exists()


class UserCreateSerializer(UserCreateSerializer):
    username = serializers.RegexField(r"^[\w.@+-]+\Z")

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )

    def validate_username(self, value):
        if len(value) > 150:
            raise serializers.ValidationError(
                'Длина поля "username" не должна превышать 150 символов'
            )
        return value


class FollowersSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="author.email", read_only=True)
    id = serializers.IntegerField(source="author.id", read_only=True)
    username = serializers.CharField(source="author.username", read_only=True)
    first_name = serializers.CharField(
        source="author.first_name", read_only=True
    )
    last_name = serializers.CharField(
        source="author.last_name", read_only=True
    )
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Followers
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )

    def get_is_subscribed(self, obj):
        return Followers.objects.filter(subscriber=obj.subscriber).exists()

    def get_recipes(self, obj):
        recipes = obj.subscriber.recipes_set.all()
        return ShortRecipesSerializer(recipes, many=True).data

    def get_recipes_count(self, obj):
        return obj.subscriber.recipes_set.count()
