from django.urls import path
from .views import IngredientsViewSet

urlpatterns = [
    path('', IngredientsViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', IngredientsViewSet.as_view({'get': 'retrieve'})),
]
