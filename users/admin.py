from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "staff_type", "is_staff")
    list_filter = ("role", "staff_type", "is_staff", "is_superuser")
    fieldsets = UserAdmin.fieldsets + (
        ("PawSmart", {"fields": ("role", "staff_type", "phone")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("PawSmart", {"fields": ("role", "staff_type", "phone")}),
    )
