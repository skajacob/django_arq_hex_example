# Librerías de Terceros
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

# Proyecto
from .models import Administrator


@admin.register(Administrator)
class UserAdmin(UserAdmin):
    ordering = ["id"]
    list_display = ["id", "email", "password", "is_staff", "is_superuser"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        ("Personal Info", {"fields": ("name",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
