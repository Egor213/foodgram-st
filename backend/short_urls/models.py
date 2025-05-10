from django.db import models
from django.conf import settings
import random


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
                self.short_url = "".join(
                    random.choices(
                        settings.CHARACTERS_SHORT_URL,
                        k=settings.TOKEN_LENGTH_SHORT_URL,
                    )
                )
                if not ShortUrl.objects.filter(
                    short_url=self.short_url
                ).exists():
                    break
        super().save(*args, **kwargs)
