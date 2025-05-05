import pytest
from django.test import Client
from pytest_django import asserts
from django.urls import reverse
from rest_framework import status

from apps.movies.models import Movies


@pytest.fixture
def get_url():
    movie = Movies.objects.all()[0]
    return reverse('movies-detail', kwargs={'pk': movie.pk})


@pytest.mark.django_db()
class TestDetailMoviesView:
    client = Client()
    model = Movies

    def test_detail_movies_status_code(self, get_url):
        response = self.client.get(get_url)
        assert response.status_code == status.HTTP_200_OK

    def test_detail_movies_template(self, get_url):
        response = self.client.get(get_url)
        asserts.assertTemplateUsed(response, 'movies/detail.html')

    def test_detail_movies_is_not_empty(self, get_url):
        response = self.client.get(get_url)
        assert response.context['movie']

