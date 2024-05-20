from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import RecipesFilter
from .models import FavoriteRecipe, Recipes, ShoppingCart
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    RecipesCreateSerializer,
    RecipesSerializer,
    ShortRecipesSerializer,
)


class RecipesViewSet(viewsets.ModelViewSet):
    filterset_class = RecipesFilter
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
            FavoriteRecipe.objects.filter(
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

    @action(methods=["get"], detail=False)
    def download_shopping_cart(self, request):

        sums = defaultdict(int)

        recipes = ShoppingCart.objects.filter(user=request.user).values(
            "recipes__ingredients__name",
            "recipes__ingredients__measurement_unit",
            "recipes__recipe_ingredients__amount",
        )

        shoping_list = []

        for recipe in recipes:
            name = recipe["recipes__ingredients__name"]
            unit = recipe["recipes__ingredients__measurement_unit"]
            amount = recipe["recipes__recipe_ingredients__amount"]
            shoping_list.append((name, amount, unit))

        for name, amount, unit in shoping_list:
            sums[(name, unit)] += amount

        summed_ingredients = [
            (name, amount, unit) for (name, unit), amount in sums.items()
        ]

        response = HttpResponse(content_type="text/plain; charset=utf-8")
        response["Content-Disposition"] = (
            'attachment; filename="shopping_list.txt"'
        )
        response.write(f"Список покупок для {request.user.username}:\n")

        for name, amount, unit in summed_ingredients:
            response.write(f"{name} - {amount} {unit}\n")

        return response
