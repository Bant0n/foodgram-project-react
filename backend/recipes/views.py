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
        recipe = get_object_or_404(Recipes, pk=pk)
        _, created = ShoppingCart.objects.get_or_create(
            user=request.user, recipes=recipe
        )
        if created:
            serializer = ShortRecipesSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "Рецепт уже добавлен в корзину."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipes, pk=pk)
        shopping_cart_item = ShoppingCart.objects.filter(
            user=request.user, recipes=recipe
        ).exists()

        if shopping_cart_item:
            ShoppingCart.objects.filter(
                user=request.user, recipes=recipe
            ).delete()
            return Response(
                {"detail": "Рецепт удален из списка покупок."},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            {"detail": "Рецепта нет в списке покупок."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(methods=["post"], detail=True)
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipes, pk=pk)
        _, created = FavoriteRecipe.objects.get_or_create(
            user=request.user, recipes=recipe
        )

        if created:
            serializer = ShortRecipesSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            {"detail": "Рецепт уже добавлен в избранное."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipes, pk=pk)
        favorite_cart_item = FavoriteRecipe.objects.filter(
            user=request.user, recipes=recipe
        ).exists()

        if favorite_cart_item:
            ShoppingCart.objects.filter(
                user=request.user, recipes=recipe
            ).delete()
            return Response(
                {"detail": "Рецепт удален из списка избранного."},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            {"detail": "Рецепта нет в списке избранного."},
            status=status.HTTP_400_BAD_REQUEST,
        )
