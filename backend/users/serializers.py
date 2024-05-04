from rest_framework import serializers
from .models import CustomUser, Followers
from djoser.serializers import UserSerializer, UserCreateSerializer


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
        return False


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
        print(value)
        if len(value) > 150:
            raise serializers.ValidationError(
                'Длина поля "username" не должна превышать 150 символов'
            )
        return value


class FollowersSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Followers
        fields = ("author",)
