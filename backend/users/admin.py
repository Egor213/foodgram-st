from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Subscription


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    search_fields = ("username", "email")
    search_help_text = "Поиск по нику или электронной почте"


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "author",
    )
    search_fields = ("user__username", "author__username")
