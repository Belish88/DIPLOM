from django.contrib import admin

from app_auth.models import Auth


@admin.register(Auth)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'phone')
