from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import FavoriteRecipe, Recipes, ShoppingCart
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    RecipesCreateSerializer,
    RecipesSerializer,
    ShortRecipesSerializer,
)


class RecipesViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthorOrReadOnly,
    ]
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("author",)

    def get_queryset(self):
        user_id = self.request.user.id
        if user_id is not None:
            qs = Recipes.favorite_and_shopping_cart.favorite_and_shopping_cart(
                user_id
            )
        else:
            qs = Recipes.objects.all()
        return qs

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return RecipesCreateSerializer
        return RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=["post"], detail=True)
    def shopping_cart(self, request, pk=None):
        instance_recipe = get_object_or_404(Recipes, pk=pk)
        ShoppingCart.objects.get_or_create(
            user=request.user, recipes=instance_recipe
        )
        serializer = ShortRecipesSerializer(instance_recipe)
        print(instance_recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipes, pk=pk)
        ShoppingCart.objects.filter(user=request.user, recipes=recipe).delete()
        return Response(
            {"detail": "Рецепт удален из списка покупок."},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(methods=["post"], detail=True)
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipes, pk=pk)
        FavoriteRecipe.objects.get_or_create(
            user=request.user, recipes=recipe
        )

        serializer = ShortRecipesSerializer(recipe)
        print(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipes, pk=pk)
        FavoriteRecipe.objects.filter(
            user=request.user, recipes=recipe
        ).delete()
        return Response(
            {"detail": "Рецепт удален из избранного."},
            status=status.HTTP_204_NO_CONTENT,
        )
