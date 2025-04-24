import pytest
from django.test import Client
from pytest_django import asserts
from django.urls import reverse
from rest_framework import status

from apps.movies.models import Movies


@pytest.mark.django_db()
class TestDetailMoviesView:
    client = Client()
    model = Movies

    def get_url(self):
        movie = self.model.objects.all()[0]
        return reverse('movies-detail', kwargs={'pk': movie.pk})

    def test_detail_movies_status_code(self):
        response = self.client.get(self.get_url())
        assert response.status_code == status.HTTP_200_OK

    def test_detail_movies_template(self):
        response = self.client.get(self.get_url())
        asserts.assertTemplateUsed(response, 'movies/detail.html')

    def test_detail_movies_is_not_empty(self):
        response = self.client.get(self.get_url())
        assert response.context['movie']

