from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Recipes, ShoppingCart, FavoriteRecipe
from .serializers import RecipesSerializer, RecipesCreateSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipes.objects.all()
    # serializer_class = RecipesSerializer

    def get_serializer_class(self):
        if self.action in ("create", "update"):
            return RecipesCreateSerializer
        return RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=["post", "delete"], detail=True)
    def add_shopping_cart(self, request, pk=None):
        try:
            recipe = Recipes.objects.get(pk=pk)
        except Recipes.DoesNotExist:
            return Response(
                {"detail": "Рецепт не найден."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.method == "DELETE":
            ShoppingCart.objects.filter(
                user=request.user, recipes=recipe
            ).delete()
            return Response(
                {"detail": "Рецепт удален из списка покупок."},
                status=status.HTTP_204_NO_CONTENT,
            )

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

    @action(methods=["post", "delete"], detail=True)
    def favorite(self, request, pk=None):
        try:
            recipe = Recipes.objects.get(pk=pk)
        except Recipes.DoesNotExist:
            return Response(
                {"detail": "Рецепт не найден."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.method == "DELETE":
            FavoriteRecipe.objects.filter(
                user=request.user, recipes=recipe
            ).delete()
            return Response(
                {"detail": "Рецепт удален из избранного."},
                status=status.HTTP_204_NO_CONTENT,
            )

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
