from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.cache import cache

from apps.directors.models import Directors


class Movies(models.Model):
    class MediaContent(models.TextChoices):
        SERIAL = 'SERIAL', 'Сериал'
        MOVIE = 'MOVIE', 'Фильм'

    position = models.IntegerField(verbose_name='Позиция', unique=True, )
    title_ru = models.CharField(verbose_name='Название на русском', )
    title_en = models.CharField(verbose_name='Название на английском', )
    release_date = models.DateTimeField(verbose_name='Дата выхода', )
    timing = models.IntegerField(verbose_name='Длительность', )
    director = models.ForeignKey(
        Directors,
        on_delete=models.CASCADE,
        verbose_name='Режиссёр',
    )
    trailer = models.URLField(verbose_name='Трейлер', )
    description = models.TextField(verbose_name='Описание', )
    poster = models.ImageField(
        verbose_name='Постер',
        upload_to='posters/%Y/%m/%d',
        default='posters/Out_Of_Poster.jpg',
        blank=True,
        null=True,
    )
    content = models.CharField(
        verbose_name='Медиа формат',
        choices=MediaContent.choices,
        default=MediaContent.MOVIE,
        blank=True,
    )
    created_at = models.DateTimeField(verbose_name='Создан', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Изменён', auto_now=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['position']
        indexes = [
            models.Index(fields=['title_ru']),
            models.Index(fields=['title_en']),
        ]
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return f'{self.title_ru}|{self.title_en}'

    def get_absolute_url(self):
        return reverse('movies-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.title_en)
            if Movies.objects.filter(position=self.position).exists():
                movies = Movies.objects.filter(position__gte=self.position)
                if movies:
                    for movie in movies.order_by('-position'):
                        movie.position = movie.position + 1
                        movie.save()
        super().save(*args, **kwargs)
