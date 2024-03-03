from django.urls import path, include
from .views import RecipesViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('recipes', RecipesViewSet)

urlpatterns = [
    # recipes
    path('', include(router.urls)),

    # shopping_cart
    # path('shop/', AddToShoppingCartView.as_view()),
]
