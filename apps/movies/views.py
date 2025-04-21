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
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import F

from apps.movies.models import Movies
from apps.movies.forms import MoviesForm, SearchForm, ViewedForm


class CreateMoviesView(PermissionRequiredMixin, View):
    template_name = 'movies/create.html'
    model = Movies
    form_class = MoviesForm
    permission_required = "movies.add_movies"

    def get(self, request):
        return render(request, self.template_name, {'form': self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            self.model.objects.create(**form.cleaned_data)
            cache.clear()
            return redirect('movies-created')
        return render(request, self.template_name, {'form': form})


class CreatedMoviesView(PermissionRequiredMixin, View):
    template_name = 'movies/created.html'
    permission_required = "movies.add_movies"

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
        viewed_movies = request.user.viewed.all()
        if cached_queryset is None:
            cache.set(full_path, queryset, timeout=5)
            paginator = Paginator(queryset, 10)
        else:
            paginator = Paginator(cached_queryset, 10)

        data = {
            'pages_movies': paginator.get_page(request.GET.get('page')),
            'form': self.form_class(),
            'query': request.GET.get('query', ''),
            'buttons_crud': {
                'Изменить': 'movies-update',
                'Удалить': 'movies-delete'
            },
            'button_auth': {'Войти': 'login'},
            'viewed_movies': viewed_movies
        }
        return render(request, self.template_name, data)


class DetailMoviesView(View):
    template_name = 'movies/detail.html'
    model = Movies

    def get(self, request, *args, **kwargs):
        movie = get_object_or_404(self.model, pk=kwargs['pk'])
        return render(request, self.template_name, {'movie': movie})


class UpdateMoviesView(PermissionRequiredMixin, View):
    template_name = 'movies/update.html'
    model = Movies
    form_class = MoviesForm
    permission_required = "movies.change_movies"

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


class DeleteMoviesView(PermissionRequiredMixin, View):
    model = Movies
    permission_required = "movies.delete_movies"

    def get(self, request, *args, **kwargs):
        movie_to_delete = self.model.objects.get(pk=kwargs['pk'])
        movies = self.model.objects.filter(
            position__gt=movie_to_delete.position,
        )
        movie_to_delete.delete()
        if movies and movie_to_delete.position > 0:
            for movie in movies:
                movie.position = movie.position - 1
                movie.save()
        cache.clear()
        return redirect('movies-list')


class ViewedView(View):
    model = Movies
    form_class = ViewedForm

    def get(self, request, *args, **kwargs):
        full_path = request.get_full_path()
        movie = self.model.objects.get(pk=kwargs['pk'])
        try:
            request.user.viewed.get(id=movie.id)
            request.user.viewed.remove(movie)
        except self.model.DoesNotExist:
            movie.user_set.add(request.user)
        finally:
            return redirect(request.GET.get('page', '/'))
