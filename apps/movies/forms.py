from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.directors.models import Directors
from apps.movies.models import Movies


class MoviesForm(forms.Form):
    position = forms.IntegerField(label='Позиция')
    title_ru = forms.CharField(label='Название на русском языке')
    title_en = forms.CharField(label='Название на английском языке')
    release_date = forms.DateTimeField(
        label='Дата выхода',
        widget=forms.DateInput(format='%d-%m-%Y', attrs={'type': 'date'}),
    )
    timing = forms.IntegerField(label='Длительность')
    director = forms.ModelChoiceField(
        queryset=Directors.objects.all(),
        label='Режиссёр',
        empty_label="Выберите режиссёра"
    )
    trailer = forms.URLField(label='Ссылка на трейлер', widget=forms.URLInput)
    description = forms.CharField(label='Описание', widget=forms.Textarea)
    poster = forms.ImageField(label='Постер')
    content = forms.ChoiceField(label='Контент', choices=Movies.MediaContent)


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Поиск',
        required=False,
        widget=forms.TextInput(attrs={"class":"search_form"})
    )