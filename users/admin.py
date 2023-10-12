from django.contrib import admin
from django.contrib.auth.models import Group

from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active']
    list_filter = ['created', 'updated']
    search_fields = ['email', 'first_name', 'last_name']
    # list_display_links = ['first_name']


admin.site.unregister(Group)
admin.site.register(models.Skill)
admin.site.register(models.Message)
