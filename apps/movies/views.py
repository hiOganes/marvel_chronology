from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.paginator import Paginator
from django.core.cache import cache
from django.contrib.postgres.search import (
    SearchQuery, SearchRank, SearchVector
)
from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import get_object_or_404
from django.urls import reverse

from apps.movies.models import Movies
from apps.movies.forms import MoviesForm, SearchForm


class CreateMoviesView(View):
    template_name = 'movies/create.html'
    model = Movies
    form_class = MoviesForm

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.model.objects.create(**form.cleaned_data)
            cache.clear()
            return redirect('movies-created')
        return render(request, self.template_name, {'form': form})


class CreatedMoviesView(View):
    template_name = 'movies/created.html'

    def get(self, request):
        return render(request, self.template_name)


class ListMoviesView(View):
    template_name = 'movies/list.html'
    model = Movies
    form_class = SearchForm

    def get_objects(self, query=None):
        if query:
            form = self.form_class(self.request.GET)
            if form.is_valid():
                query = form.cleaned_data.get('query')
                queryset = self.model.objects.annotate(
                    similarity=TrigramSimilarity('title_ru', query) +
                               TrigramSimilarity('title_en', query)
                ).filter(
                    similarity__gte=0.1).order_by(
                    '-similarity'
                ).select_related('director')
            return queryset
        else:
            return self.model.objects.all(
            ).select_related('director')

    def get(self, request):
        full_path = request.get_full_path()
        queryset = self.get_objects(request.GET.get('query', None))
        cached_queryset = cache.get(full_path, None)
        if cached_queryset is None:
            cache.set(full_path, queryset, timeout=5)
            paginator = Paginator(queryset, 2)
        else:
            paginator = Paginator(cached_queryset, 2)
        data = {
            'pages_movies': paginator.get_page(request.GET.get('page')),
            'form': self.form_class(),
            'query': request.GET.get('query', ''),
            'buttons_crud': {
                'Изменить': 'movies-update',
                'Удалить': 'movies-delete'
            },
            'button_auth': {'Войти': 'login'},
        }
        return render(request, self.template_name, data)


class DetailMoviesView(View):
    template_name = 'movies/detail.html'
    model = Movies

    def get(self, request, *args, **kwargs):
        movie = get_object_or_404(self.model, pk=kwargs['pk'])
        return render(request, self.template_name, {'movie': movie})


class UpdateMoviesView(View):
    template_name = 'movies/update.html'
    model = Movies
    form_class = MoviesForm

    def get(self, request, *args, **kwargs):
        movie = get_object_or_404(self.model, pk=kwargs['pk'])
        form = self.form_class({**movie.__dict__})
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            movie = self.model.objects.get(pk=kwargs['pk'])
            for key, value in form.cleaned_data.items():
                setattr(movie, key, value)
            if 'poster' in request.FILES:
                movie.poster = request.FILES['poster']
            movie.save()
            cache.clear()
            return redirect(
                reverse('movies-detail', kwargs={'pk': kwargs['pk']}),
            )
        return render(request, self.template_name, {'form': form})


class DeleteMoviesView(View):
    model = Movies

    def get(self, request, *args, **kwargs):
        self.model.objects.get(pk=kwargs['pk']).delete()
        cache.clear()
        return redirect('movies-list')

