from django.db import models

from short_urls.services import generate_short_url


class ShortUrl(models.Model):
    origin_url = models.URLField(
        verbose_name="Исходная ссылка", primary_key=True
    )
    short_url = models.SlugField(
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
            self.short_url = generate_short_url()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.short_url
