from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import FavoriteRecipe, Recipes, ShoppingCart
from .serializers import RecipesCreateSerializer, RecipesSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = RecipesSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        "author",
    )

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
        return Response(
            {"detail": "Рецепт уже находится в корзине."},
            status=status.HTTP_400_BAD_REQUEST,
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
        return Response(
            {"detail": "Рецепт уже находится в избранном."},
            status=status.HTTP_400_BAD_REQUEST,
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
