from django.contrib import admin
from .models import Profile
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'bio', 'phone_number']
    search_fields = ['username__istartswith']
    list_per_page = 10


admin.site.register(Profile, ProfileAdmin)
