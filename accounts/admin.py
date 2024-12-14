from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        *UserAdmin.fieldsets,  # 既存のフィールドセットを展開
        ("Custom Fields", {"fields": ("icon_image", "introduction", "following", "terms_of_service_version")}),
    )

    add_fieldsets = (
        *UserAdmin.fieldsets,  # 既存のフィールドセットを展開
        ("Custom Fields", {"fields": ("icon_image", "introduction", "following", "terms_of_service_version")}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
