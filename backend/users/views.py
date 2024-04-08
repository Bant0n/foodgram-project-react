from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Followers, CustomUser
from .serializers import FollowersSerializer


class UserViewSet(UserViewSet):
    @action(detail=True, methods=["post"])
    def subscribe(self, request, id=None):
        author = get_object_or_404(CustomUser, id=id)

        subscriber = self.request.user
        follow, created = Followers.objects.get_or_create(
            author=author, subscriber=subscriber
        )
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
