from django.db import models
from pytils.translit import slugify


class Tag(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=8, blank=True)
    slug = models.SlugField(blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
