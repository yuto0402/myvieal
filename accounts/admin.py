from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = (
        *UserAdmin.fieldsets,  # 既存のフィールドセットを展開
        ('Custom Fields', {'fields': ("icon_image", "introduction",)})
    )

    add_fieldsets = (
        *UserAdmin.fieldsets,  # 既存のフィールドセットを展開
        ('Custom Fields', {'fields': ("icon_image", "introduction",)})
    )


admin.site.register(CustomUser, CustomUserAdmin)
