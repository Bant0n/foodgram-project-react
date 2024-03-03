from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Followers(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="followers"
    )

    def __str__(self) -> str:
        return f'На {self.author} подписан {self.subscriber}'
