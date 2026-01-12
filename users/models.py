from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True,
        verbose_name="Photo de profil",
    )

    def __str__(self):
        return self.username or self.email
