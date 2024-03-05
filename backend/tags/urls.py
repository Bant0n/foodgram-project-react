from django.urls import path
from .views import TagViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('tags', TagViewSet)

# urlpatterns = [
#     path('', TagViewSet.as_view({'get': 'list'})),
#     path('<int:pk>/', TagViewSet.as_view({'get': 'retrieve'})),
# ]
