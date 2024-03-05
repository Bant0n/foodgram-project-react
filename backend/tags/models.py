from django.db import models
from pytils.translit import slugify


class Tag(models.Model):
    name = models.CharField(max_length=16, verbose_name="Название")
    color = models.CharField(
        max_length=8, blank=True, verbose_name="Цвет в HEX формате"
    )
    slug = models.SlugField(blank=True, verbose_name="Уникальный слаг")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
