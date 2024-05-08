from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import Recipes
from recipes.serializers import ShortRecipesSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from .models import CustomUser, Followers
from .serializers import FollowersSerializer


class UserViewSet(UserViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=["post"])
    def subscribe(self, request, id=None):
        author = get_object_or_404(CustomUser, id=id)
        if author == self.request.user:
            return Response(
                {"errors": "Нельзя подписаться на себя."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        recipes = Recipes.objects.filter(author=author)
        subscriber = self.request.user
        _, created = Followers.objects.get_or_create(
            author=subscriber, subscriber=author
        )
        if created:
            return Response(
                {
                    "email": author.email,
                    "id": author.id,
                    "username": author.username,
                    "first_name": author.first_name,
                    "last_name": author.last_name,
                    "is_subscribed": created,
                    "recipes": ShortRecipesSerializer(recipes, many=True).data,
                    "recipes_count": author.recipes_set.count(),
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"errors": "Вы уже подписаны на этого пользователя."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        author = get_object_or_404(CustomUser, id=id)
        Followers.objects.filter(author=author).delete()
        return Response(
            {"detail": "Вы отписались от пользователя."},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(
        detail=False,
        methods=["get"],
    )
    def subscriptions(self, request):
        qs = self.filter_queryset(
            Followers.objects.filter(author=request.user)
        )
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = FollowersSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(qs.data)

    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        self.get_object = self.get_instance
        return self.retrieve(request)
