from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser
# Register your models here.


class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", "email", "first_name", "last_name"),
            },
        ),
    )

    list_display = [
        'username', 'email', 'first_name', 'last_name', 'is_staff']
    search_fields = ['username__istartswith', 'first_name__istartswith',
                     'last_name__istartswith']
    ordering = ['first_name', 'last_name']
    list_per_page = 10


admin.site.register(CustomUser, UserAdmin)
