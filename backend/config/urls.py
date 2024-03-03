from django.contrib import admin
from django.urls import path, include
from users.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),

    # users
    # path('api/', include('djoser.urls')),
    path('api/', include(router.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),

    # tags
    path('api/tags/', include('tags.urls')),

    # ingredients
    path('api/ingredients/', include('ingredients.urls')),

    # recipes
    path('api/', include('recipes.urls')),
]
