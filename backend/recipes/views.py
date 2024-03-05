from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import FavoriteRecipe, Recipes, ShoppingCart
from .serializers import RecipesCreateSerializer, RecipesSerializer
from django.shortcuts import get_object_or_404


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()

    def get_queryset(self):
        if self.request.user.is_authenticated:
            qs = Recipes.favorite_and_shopping_cart.favorite_and_shopping_cart(
                self.request.user
            )
        else:
            qs = Recipes.objects.all()
        return qs

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return RecipesCreateSerializer
        return RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=["post"], detail=True)
    def add_shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipes, pk=pk)

        shopping_cart_item, created = ShoppingCart.objects.get_or_create(
            user=request.user, recipes=recipe
        )

        if created:
            return Response(
                {"detail": "Рецепт добавлен в корзину."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"detail": "Рецепт уже находится в корзине."},
                status=status.HTTP_200_OK,
            )

    @add_shopping_cart.mapping.delete
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

        favorite, created = FavoriteRecipe.objects.get_or_create(
            user=request.user, recipes=recipe
        )

        if created:
            return Response(
                {"detail": "Рецепт добавлен в избранное."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"detail": "Рецепт уже находится в избранном."},
                status=status.HTTP_200_OK,
            )

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
