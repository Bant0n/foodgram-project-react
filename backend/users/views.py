from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .serializers import FollowersSerializer
from .models import Followers, User


class UserViewSet(UserViewSet):
    @action(detail=True, methods=["post", "delete", "get"])
    def subscribe(self, request, id=None):
        try:
            # author = self.get_object()
            author = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(
                {"detail": "Пользователь не найден."},
                status=status.HTTP_404_NOT_FOUND,
            )
        # author = self.get_object()

        if request.method == "DELETE":
            Followers.objects.filter(author=author).delete()
            return Response(
                {"detail": "Вы отписались от пользователя."},
                status=status.HTTP_204_NO_CONTENT,
            )

        print(author)
        subscriber = self.request.user
        print(subscriber)
        follow, created = Followers.objects.get_or_create(
            author=author, subscriber=subscriber
        )
        print(follow)
        if created:
            return Response(
                {"detail": "Вы подписались на пользователя."},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"detail": "Вы уже подписаны на пользователя."},
                status=status.HTTP_200_OK,
            )

    @action(detail=False, methods=["get"])
    def subscriptions(self, request):
        qs = Followers.objects.filter(subscriber=self.request.user)
        serializer = FollowersSerializer(qs, many=True)
        print(serializer.data)
        return Response(
            {
                "count": qs.count(),
                "subscriptions": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
