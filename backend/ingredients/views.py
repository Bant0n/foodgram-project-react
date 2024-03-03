from .models import Ingredients
from .serializers import IngredientsSerializer
from rest_framework import viewsets


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
