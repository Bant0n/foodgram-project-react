from django.shortcuts import get_object_or_404

# from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.serializers import ShortRecipesSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from recipes.models import Recipes
from .models import CustomUser, Followers
from .serializers import FollowersSerializer


class UserViewSet(UserViewSet):
    permission_classes = [AllowAny]
    # filter_backends = (DjangoFilterBackend, )
    # filterset_fields = ("author",)

    @action(detail=True, methods=["post"])
    def subscribe(self, request, id=None):
        author = get_object_or_404(CustomUser, id=id)
        recipes = Recipes.objects.filter(author=author)
        print(recipes)
        print(author.recipes_set.all())
        subscriber = self.request.user
        _, created = Followers.objects.get_or_create(
            author=author, subscriber=subscriber
        )
        if created:
            return Response(
                {
                    "email": author.email,
                    "id": author.id,
                    "username": author.username,
                    "first_name": author.first_name,
                    "last_name": author.last_name,
                    "is_subscribed": created,
                    "recipes": ShortRecipesSerializer(recipes, many=True).data,
                    "recipes_count": author.recipes_set.count(),
                },
                status=status.HTTP_201_CREATED,
            )
        # else:
        #     return Response(
        #         {
        #             "email": author.email,
        #             "id": author.id,
        #             "username": author.username,
        #             "first_name": author.first_name,
        #             "last_name": author.last_name,
        #             "is_subscribed": created,
        #             "recipes": ShortRecipesSerializer(recipes, many=True).data,
        #             "recipes_count": author.recipes_set.count(),
        #         },
        #         status=status.HTTP_201_CREATED,
        #     )
        else:
            return Response(
                {"errors": "Вы уже подписаны на этого пользователя."},
                status=status.HTTP_400_BAD_REQUEST
            )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id=None):
        author = get_object_or_404(CustomUser, id=id)
        Followers.objects.filter(author=author).delete()
        return Response(
            {"detail": "Вы отписались от пользователя."},
            status=status.HTTP_204_NO_CONTENT,
        )

    @action(detail=False, methods=["get"])
    def subscriptions(self, request):
        qs = self.request.user.followers.all()
        serializer = FollowersSerializer(qs, many=True)
        return Response(
            {
                "count": qs.count(),
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        self.get_object = self.get_instance
        return self.retrieve(request)
