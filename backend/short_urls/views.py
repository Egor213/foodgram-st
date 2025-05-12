from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView

from .models import ShortUrl


class ShortUrlAPIView(APIView):

    def get(self, request, short_url):
        short_url = f"/s/{short_url}/"
        obj = get_object_or_404(ShortUrl, short_url=short_url)
        return HttpResponseRedirect(
            request.build_absolute_uri(f"{obj.origin_url}")
        )
