from django_filters import rest_framework as filter
from .models import Recipes


class RecipesFilter(filter.FilterSet):
    is_favorited = filter.BooleanFilter(method="get_is_favorited")
    is_in_shopping_cart = filter.BooleanFilter(
        method="get_is_in_shopping_cart"
    )
    tags = filter.CharFilter(field_name="tags__slug")

    class Meta:
        model = Recipes
        fields = ["tags"]

    def get_is_favorited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favoriterecipe__user=self.request.user)
        return queryset

    def get_is_in_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(shoppingcart__user=self.request.user)
        return queryset
