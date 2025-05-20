import random

from django.conf import settings


def generate_short_url():
    from short_urls.models import ShortUrl

    while True:
        token = "".join(
            random.choices(
                settings.CHARACTERS_SHORT_URL,
                k=settings.TOKEN_LENGTH_SHORT_URL,
            )
        )
        short_url = f"/s/{token}/"
        if not ShortUrl.objects.filter(short_url=short_url).exists():
            return short_url
