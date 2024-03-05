from rest_framework import serializers
from .models import CustomUser, Followers


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            'is_subscribed'
        )
        extra_kwargs = {"password": {"write_only": True}}

    def get_is_subscribed(self, obj):
        return False


class FollowersSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Followers
        fields = ("author",)
