from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager


class User(AbstractUser):
    username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("Username"),
        validators=[UnicodeUsernameValidator()],
    )
    email = models.EmailField(
        unique=True,
        help_text=_("Required and unique."),
        verbose_name=_("Email address"),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.email} ({self.pk})"
