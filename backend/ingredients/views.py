from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Ingredients
from .serializers import IngredientsSerializer


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ("name",)
    search_fields = ("name",)
    pagination_class = None
