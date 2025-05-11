from django.urls import path

from .views import ShortUrlAPIView

app_name = "short_urls"

urlpatterns = [
    path("s/<str:short_url>/", ShortUrlAPIView.as_view()),
]
