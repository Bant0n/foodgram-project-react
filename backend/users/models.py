from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    username = models.CharField(
        max_length=150, unique=True, verbose_name="Ник-нейм пользователя"
    )
    email = models.EmailField(
        blank=False, unique=True, verbose_name="Электронная почта"
    )
    first_name = models.CharField("Имя", max_length=128)
    last_name = models.CharField("Фамилия", max_length=128)


class Followers(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="following"
    )
    subscriber = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="followers"
    )

    def __str__(self) -> str:
        return f"На {self.author} подписан {self.subscriber}"
