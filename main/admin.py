from django.contrib import admin

from . import models


admin.site.register(models.Project)
admin.site.register(models.Tag)
admin.site.register(models.Review)
