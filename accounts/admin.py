from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["id", "username", "password", "email", "icon_image", "introduction", "date_joined"]


admin.site.register(CustomUser, CustomUserAdmin)
