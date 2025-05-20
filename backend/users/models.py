from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models


class CustomUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    email = models.EmailField(
        verbose_name="Электронная почта",
        unique=True,
        max_length=settings.MAX_LEN_USER_EMAIL,
        help_text="Адрес электронной почты",
    )
    username = models.CharField(
        verbose_name="Ник пользоваля",
        unique=True,
        max_length=settings.MAX_LEN_USER_USERNAME,
        validators=[username_validator],
    )
    last_name = models.CharField(
        verbose_name="Фамилия пользоваля",
        max_length=settings.MAX_LEN_USER_LAST_NAME,
    )
    first_name = models.CharField(
        verbose_name="Имя пользоваля",
        max_length=settings.MAX_LEN_USER_FIRST_NAME,
    )
    avatar = models.ImageField(
        verbose_name="Аватар",
        upload_to=getattr(settings, "UPLOAD_AVATAR", "users/images/"),
        null=True,
        blank=True,
        default=None,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class Subscription(models.Model):
    user = models.ForeignKey(
        verbose_name="Пользователь",
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    author = models.ForeignKey(
        verbose_name="Отслеживаемый автор",
        to=CustomUser,
        on_delete=models.CASCADE,
        related_name="subscribers",
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=("user", "author"), name="unique_following"
            ),
        )
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    def clean(self):
        if self.user == self.author:
            raise ValidationError("Нельзя подписаться на самого себя.")
        return super().clean()

    def __str__(self):
        return f"{self.user}"
