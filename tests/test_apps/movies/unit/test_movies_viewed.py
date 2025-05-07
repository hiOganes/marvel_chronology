import pytest
from django.test import Client
from pytest_django import asserts
from django.urls import reverse
from rest_framework import status

from apps.movies.models import Movies


@pytest.fixture
def get_url():
    movie = Movies.objects.all()[0]
    return reverse('movies-viewed', kwargs={'pk': movie.pk})


@pytest.mark.django_db()
class TestViewedMoviesView:
    client = Client()
    model = Movies

    def test_viewed_movies_status_code(self, get_url, login_data):
        self.client.login(**login_data['user'])
        response = self.client.get(get_url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_viewed_movies_add(self, login_data):
        self.client.login(**login_data['superuser'])
        movie = self.model.objects.all()[0]
        viewed_before = movie.user_set.count()
        response = self.client.get(
            reverse('movies-viewed', kwargs={'pk': movie.pk})
        )
        viewed_after = movie.user_set.count()
        assert viewed_before < viewed_after
        response = self.client.get(
            reverse('movies-viewed', kwargs={'pk': movie.pk})
        )
        viewed_after = movie.user_set.count()
        assert viewed_before == viewed_after
