from django.urls import include, path

app_name = "api"

urlpatterns = [
    path("", include("api.ingredients.urls")),
    path("", include("api.users.urls")),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
