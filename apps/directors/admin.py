from django.contrib import admin

from apps.directors.models import Directors


@admin.register(Directors)
class DirectorsAdmin(admin.ModelAdmin):
    pass
