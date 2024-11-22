from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    icon_image = models.ImageField(upload_to="user/", null=True, blank=False)
    introduction = models.TextField(blank=True)
