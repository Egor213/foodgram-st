import random

from django.conf import settings
from django.db import models


class ShortUrl(models.Model):
    origin_url = models.URLField(
        verbose_name="Исходная ссылка", primary_key=True
    )
    short_url = models.CharField(
        verbose_name="Короткая ссылка",
        max_length=20,
        unique=True,
        db_index=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Короткая ссылка"
        verbose_name_plural = "Короткие ссылки"

    def save(self, *args, **kwargs):
        if not self.short_url:
            while True:
                token = "".join(
                    random.choices(
                        settings.CHARACTERS_SHORT_URL,
                        k=settings.TOKEN_LENGTH_SHORT_URL,
                    )
                )
                self.short_url = f"/s/{token}/"
                if not ShortUrl.objects.filter(
                    short_url=self.short_url
                ).exists():
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.short_url
