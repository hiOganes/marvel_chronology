from django.contrib import admin

from apps.movies.models import Movies


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ['position', 'title_ru', 'title_en']
    list_display_links = ['position', 'title_ru', 'title_en']
    search_fields = ['title_ru', 'title_en']
    search_help_text = 'Русское или Английское название фильма'
    list_per_page = 10
