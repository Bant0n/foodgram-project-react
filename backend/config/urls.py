from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from ingredients.views import IngredientsViewSet
from recipes.views import RecipesViewSet
from rest_framework.routers import DefaultRouter
from tags.views import TagViewSet
from users.views import UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet)
router.register("tags", TagViewSet)
router.register("recipes", RecipesViewSet)
router.register("ingredients", IngredientsViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/auth/", include("djoser.urls.authtoken")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="docs",
    ),
]
