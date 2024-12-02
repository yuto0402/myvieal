from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    icon_image = models.ImageField(
        upload_to="user/",
        default="misc/722e64ef8f12418691bf75c04b83ebbe.png",
        null=True,
        blank=False,
    )
    introduction = models.TextField(blank=True)
    following = models.ManyToManyField("self", related_name="followed_by", symmetrical=False, blank=True)
